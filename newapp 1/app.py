import json
from flask import Flask, request, jsonify
from flask_cors import CORS
from services import call_openai, identify_abandoned_carts, call_openai_cart, call_openai_reviews
from models import users, products, orders, inventory, reviews
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
import os
from typing import List, Dict
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from recommendation import get_recommendation_service
import logging
from weatherfetch import (
    consolidate_delivery_cities,
    fetch_weather_data,
    group_orders_by_user,
    prepare_inventory_data,
    generate_openai_prompt,
    parse_openai_response,
    group_issues_by_user,
    send_user_emails
)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
from productreviews import create_review_prompt, get_similar_products
from indevntorydata import inventory_list
from inventory_analyzer import get_product_forecast_data


app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

class EmailSender:
    def __init__(self, smtp_server="smtp.gmail.com", smtp_port=587):
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port

    def send_email(self, sender_email, sender_password, recipient_email, subject, body, attachments=None):
        try:
            message = MIMEMultipart()
            message['From'] = sender_email
            message['To'] = recipient_email
            message['Subject'] = subject
            message.attach(MIMEText(body, 'plain'))
            if attachments:
                for file_path in attachments:
                    with open(file_path, 'rb') as file:
                        part = MIMEApplication(file.read(), Name=os.path.basename(file_path))
                        part['Content-Disposition'] = f'attachment; filename="{os.path.basename(file_path)}"'
                        message.attach(part)
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(sender_email, sender_password)
                server.send_message(message)
            return True
        except Exception as e:
            print(f"Error sending email: {str(e)}")
            return False

@app.route('/recommendation', methods=['POST'])
def get_recommendation():
    data = request.json
    email = data.get("user_id")
   
    # Map email to user ID
    user = next((user for user in users if user["Email"] == email), None)
    if not user:
        return jsonify({"error": "User not found"}), 400
   
    user_id = user["UserID"]
    response = get_recommendation_service(user_id)
    return jsonify(response), 200 if 'error' not in response else 400

@app.route('/issue', methods=['GET'])
async def issue():
    try:
        # Get email from headers
        email = request.headers.get('email')
        print(f"Email: {email}")
        if not email:
            return jsonify({"error": "Email header is missing"}), 400

        # Fetch user ID from email
        user = next((user for user in users if user["Email"] == email), None)
        if not user:
            return jsonify({"error": "User not found"}), 404

        user_id = user["UserID"]
        print(f"User ID: {user_id}")

        # Consolidate all delivery cities
        delivery_cities = await consolidate_delivery_cities(orders)

        # Fetch weather data for all cities asynchronously
        weather_data = await fetch_weather_data(delivery_cities)

        # Group orders by user
        orders_by_user = group_orders_by_user(orders)

        # Prepare inventory data
        inventory_by_city = prepare_inventory_data(inventory)

        # Create prompt for OpenAI
        prompt = generate_openai_prompt(orders_by_user, inventory_by_city, weather_data)

        # Call OpenAI
        analysis_result = call_openai(prompt)

        # Parse OpenAI response
        parsed_result = parse_openai_response(analysis_result)

        # Group issues by user
        issues_by_user = group_issues_by_user(parsed_result)

        # Identify on-time orders
        issue_order_ids = {issue["OrderID"] for issue in parsed_result}
        on_time_orders = []
        for order in orders:
            if order["OrderID"] not in issue_order_ids and "Products" in order and "UserID" in order:
                for product in order["Products"]:
                    if "ProductID" in product:
                        on_time_orders.append({
                            "OrderID": order["OrderID"],
                            "ProductID": product["ProductID"],
                            "UserID": order["UserID"]
                        })

        # Filter responses for the specific user ID
        filtered_issues = [issue for issue in parsed_result if issue["UserID"] == user_id]
        filtered_on_time_orders = [order for order in on_time_orders if order["UserID"] == user_id]

        # # Send emails to users
        # await send_user_emails(users, orders, products, issues_by_user, EmailSender())

        return jsonify({
            "issues": filtered_issues,
            "on_time_orders": filtered_on_time_orders
        }), 200

    except ValueError as ve:
        return jsonify({"error": str(ve)}), 500
    except Exception as e:
        return jsonify({"error": "An unexpected error occurred", "details": str(e)}), 500

@app.route('/cart-management', methods=['GET'])
def cart_management():
    try:
        # Step 1: Identify users with abandoned carts
        abandoned_carts = identify_abandoned_carts()
        
        # Step 2: Prepare data for recovery actions
        recovery_data = []
        for cart in abandoned_carts:
            user = next((u for u in users if u["UserID"] == cart["UserID"]), None)
            if user:
                abandoned_items = []
                for item in cart["Products"]:
                    product = next((p for p in products if p["ProductID"] == item["ProductID"]), None)
                    if product:
                        abandoned_items.append({
                            "Title": product["Title"],
                            "Price": product["Price"],
                            "Quantity": item["Quantity"]
                        })
                recovery_data.append({
                    "UserID": user["UserID"],
                    "AbandonedItems": abandoned_items,
                })

        # Step 3: Generate recovery email content using OpenAI
        prompt = (
            f"Generate abandoned cart recovery emails for these carts:"
            f"{recovery_data}\n\n"
            "Return ONLY a JSON array with no additional text."
        )

        # print(prompt)  # Debugging purpose
        recovery_emails = call_openai_cart(prompt)

        # Step 4: Parse OpenAI response
        try:
            email_data = json.loads(recovery_emails)  # Ensure OpenAI returns structured JSON
        except json.JSONDecodeError as e:
            return jsonify({"error": "Failed to parse OpenAI response", "details": str(e)}), 500
        
        # Step 5: Send emails to users
        email_sender = EmailSender()
        sender_email = "sundramsksshri@gmail.com"
        sender_password = "vdnv poiw mcgh rtka"  # Use app password for Gmail

        for email in email_data:
            user_id = email["userId"]
            user = next((u for u in users if u["UserID"] == user_id), None)
            if not user:
                continue
            user_email = user["Email"]
            user_name = user["Name"]
            subject = email["subject"]
            body = f"Dear {user_name},\n\n{email['body']}\n\nBest Regards,\nAgentic Team"

            success = email_sender.send_email(
                sender_email=sender_email,
                sender_password=sender_password,
                recipient_email=user_email,
                subject=subject,
                body=body
            )
            if success:
                print(f"Email sent successfully to {user_email}!")
            else:
                print(f"Failed to send email to {user_email}.")

        return jsonify({"recovery_emails": email_data})
    
    except Exception as e:
        return jsonify({"error": "An unexpected error occurred", "details": str(e)}), 500

@app.route('/product-review-summary', methods=['POST'])
def generate_review_summary():
    try:
        data = request.get_json()
        
        # Validate input
        if not data or 'product_id' not in data:
            return jsonify({
                'error': 'Missing required field: product_id'
            }), 400
            
        product_id = data['product_id']
        
        # Fetch product name and reviews from the reviews table
        product = next((p for p in products if p["ProductID"] == product_id), None)
        product_reviews = next((r for r in reviews if r["ProductID"] == product_id), None)
        
        if not product or not product_reviews:
            return jsonify({
                'error': 'Product or reviews not found'
            }), 404
        
        product_name = product["Name"]
        reviews_list = product_reviews["reviews"]
        
        # Create the prompt
        prompt = create_review_prompt(product_name, reviews_list)
        
        # Call OpenAI API
        response = call_openai_reviews(prompt)

        # Get similar products (including same brand)
        similar_products = get_similar_products(products, product_id)
        
        # Extract and return the summary
        try:
            summary = response
        except (json.JSONDecodeError, KeyError, IndexError) as e:
            return jsonify({
                'error': 'Failed to parse OpenAI response',
                'details': str(e)
            }), 500
        
        return jsonify({
            'product_name': product_name,
            'summary': summary,
            'review_count': len(reviews_list),
            'similar_products': similar_products
        })
        
    except Exception as e:
        return jsonify({
            'error': f'An error occurred: {str(e)}'
        }), 500


@app.route("/forecast", methods=["POST"])
def forecast_product():
    """
    Generate forecast for a specific product by ProductID provided in the POST request body.
    """
    try:
        # Parse the JSON request body
        data = request.get_json()

        if not data or "ProductID" not in data:
            return jsonify({"error": "ProductID is required in the request body"}), 400

        product_id = data["ProductID"]

        # Search for the product in the inventory list
        product_forecast = get_product_forecast_data(inventory_list, product_id)
        if product_forecast:
            return(json.dumps(product_forecast, indent=4))

            # If product not found in any inventory
        return jsonify({"error": f"Product with ID {product_id} not found"}), 404

    except Exception as e:
        logger.error(f"Error generating forecast for ProductID: {e}")
        return jsonify({"error": "An internal server error occurred"}), 500

if __name__ == '__main__':
    app.run(debug=True)