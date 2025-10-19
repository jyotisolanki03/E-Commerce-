from flask import Flask, jsonify
import json
import requests
import asyncio
import aiohttp
from datetime import datetime, timedelta
async def fetch_weather(session, city):
    """Fetch weather data for a single city using aiohttp session"""
    api_key = "0b9c34328d21216b0b254650ef76ca26"
    url = f"https://api.weatherstack.com/current?access_key={api_key}&query={city}"
    
    try:
        async with session.get(url) as response:
            if response.status == 200:
                data = await response.json()
                return city, data["current"]["weather_descriptions"]
            else:
                return city, f"Error: Status {response.status}"
    except Exception as e:
        return city, f"Error: {str(e)}"

async def fetch_all_weather(cities):
    """Fetch weather data for all cities concurrently but wait for all results"""
    async with aiohttp.ClientSession() as session:
        # Create tasks for all cities
        tasks = [fetch_weather(session, city) for city in cities]
        # Wait for all tasks to complete
        results = await asyncio.gather(*tasks)
        
        # Convert results to dictionary
        weather_data = {}
        for city, weather in results:
            if isinstance(weather, str) and weather.startswith("Error"):
                print(f"Warning: Failed to fetch weather for {city}: {weather}")
                weather_data[city] = ["Unknown"]
            else:
                weather_data[city] = weather
                
        return weather_data
async def consolidate_delivery_cities(orders):
    return {order["DeliveryCity"] for order in orders}

async def fetch_weather_data(delivery_cities):
    # Mocking the fetch function for weather data.
    return await fetch_all_weather(delivery_cities)

def group_orders_by_user(orders):
    orders_by_user = {}
    for order in orders:
        user_id = order["UserID"]
        if user_id not in orders_by_user:
            orders_by_user[user_id] = []
        orders_by_user[user_id].append(order)
    return orders_by_user

def prepare_inventory_data(inventory):
    return {inv["DeliveryCity"]: inv for inv in inventory}

def generate_openai_prompt(orders_by_user, inventory_by_city, weather_data):
    return (
        f"Process the following data and analyze if orders are delayed due to weather conditions "
        f"(non-sunny/clear conditions) or inventory shortages:\n\n"
        f"Orders by User: {orders_by_user}\n\n"
        f"Inventory by City: {inventory_by_city}\n\n"
        f"Weather Data: {weather_data}\n\n"
        "Note: Strictly if there is no Product ID in an inventory, consider it as out of stock."
        "Note: Dont hallucinate any reason. Give correct reason only. If out of stock, mention out of stock. If bad weather, mention bad weather. If no delay, dont return it."
        "Note: Strictly return me the output array only. No need to give other details. Just return the array output as specified."
        "Note: Dont give code. Just give the output array as answer having all details as specified in example."
    )

def parse_openai_response(analysis_result):
    try:
        parsed_result = json.loads(analysis_result)
        if not isinstance(parsed_result, list):
            raise ValueError("Response is not a valid JSON array")
        return parsed_result
    except json.JSONDecodeError as e:
        raise ValueError("Failed to parse OpenAI response") from e

def group_issues_by_user(parsed_result):
    issues_by_user = {}
    for issue in parsed_result:
        user_id = issue["UserID"]
        if user_id not in issues_by_user:
            issues_by_user[user_id] = []
        issues_by_user[user_id].append(issue)
    return issues_by_user

async def send_user_emails(users, orders, products, issues_by_user, email_sender):
    sender_email = "sundramsksshri@gmail.com"
    sender_password = "vdnv poiw mcgh rtka"  # Use app password for Gmail

    for user_id, issues in issues_by_user.items():
        user = next((u for u in users if u["UserID"] == user_id), None)
        if not user:
            continue
        user_email = user["Email"]
        user_name = user["Name"]
        body = f"Dear {user_name},\n\nWe hope this message finds you well. We regret to inform you that your orders are experiencing unexpected delays due to the following reasons:\n\n"
        for issue in issues:
            order = next((o for o in orders if o["OrderID"] == issue["OrderID"]), None)
            product = next((p for p in products if p["ProductID"] == issue["ProductID"]), None)
            if order and product:
                body += f"- Order ID: {issue['OrderID']}, Product: {product['Name']} ({product['Title']}), Reason: {issue['Reason']}\n"
        body += "\nWe understand how important these orders are to you, and we sincerely apologize for any inconvenience this may cause. Please rest assured that our team is working diligently to resolve these issues and ensure your orders reach you as quickly as possible.\n\nBest regards,\nAgentic Team"

        success = email_sender.send_email(
            sender_email=sender_email,
            sender_password=sender_password,
            recipient_email=user_email,
            subject="Update on Your Orders: Delivery Delay Notification",
            body=body
        )
        if success:
            print(f"Email sent successfully to {user_email}!")
        else:
            print(f"Failed to send email to {user_email}.")