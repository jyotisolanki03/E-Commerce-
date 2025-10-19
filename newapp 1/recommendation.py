from prompt import system_prompt_market_trend, system_prompt_user_history
import requests
import json
from config import OPENAI_API_KEY, OPENAI_API_URL
from models import products, users, browsing_history, purchase_history, cart_activity
import asyncio
import aiohttp
from datetime import datetime, timedelta

def get_recommendation_service(user_id):
    user = next((u for u in users if u["UserID"] == user_id), None)
    if not user:
        return {"error": "Invalid user_id"}

    # Get browsing history for the specific user with product details
    user_browsing_history = next((history for history in browsing_history if history["UserID"] == user_id), None)
    if user_browsing_history:
        user_browsing = []
        for browse in user_browsing_history["BrowsingList"]:
            product_details = next((p for p in products if p["ProductID"] == browse["ProductID"]), {})
            user_browsing.append({
                "ProductID": browse["ProductID"],
                "Timestamp": browse["Timestamp"],
                "ViewedTimes": browse["ViewedTimes"],
                "ActionType": browse["ActionType"],
                "ProductDetails": product_details
            })
    else:
        user_browsing = []

    # Get purchase history for the specific user with product details
    user_purchase_history = next((history for history in purchase_history if history["UserID"] == user_id), None)
    if user_purchase_history:
        user_purchases = []
        for purchase in user_purchase_history["PurchasedList"]:
            product_details = next((p for p in products if p["ProductID"] == purchase["ProductID"]), {})
            user_purchases.append({
                "ProductID": purchase["ProductID"],
                "Timestamp": purchase["Timestamp"],
                "Quantity": purchase["Quantity"],
                "ProductDetails": product_details
            })
    else:
        user_purchases = []

    # Prepare the prompt for the complete browsing and purchase history
    all_browsing_history = []
    for history in browsing_history:
        user_browsing = []
        for browse in history["BrowsingList"]:
            product_details = next((p for p in products if p["ProductID"] == browse["ProductID"]), {})
            user_browsing.append({
                "ProductID": browse["ProductID"],
                "Timestamp": browse["Timestamp"],
                "ViewedTimes": browse["ViewedTimes"],
                "ActionType": browse["ActionType"],
                "ProductDetails": product_details
            })
        all_browsing_history.append({
            "UserID": history["UserID"],
            "BrowsingList": user_browsing
        })

    all_purchase_history = []
    for history in purchase_history:
        user_purchases = []
        for purchase in history["PurchasedList"]:
            product_details = next((p for p in products if p["ProductID"] == purchase["ProductID"]), {})
            user_purchases.append({
                "ProductID": purchase["ProductID"],
                "Timestamp": purchase["Timestamp"],
                "Quantity": purchase["Quantity"],
                "ProductDetails": product_details
            })
        all_purchase_history.append({
            "UserID": history["UserID"],
            "PurchasedList": user_purchases
        })


    prompt_complete = f"""Based on the following user data, suggest personalized product recommendations:



User Profile:
- Name: {user['Name']}
- Email: {user['Email']}
- Age: {user['Age']}
- Location: {user['Location']}
- Gender: {user['Gender']}

Recent Browsing History:
{all_browsing_history}

Purchase History:
{all_purchase_history}

IMPORTANT: Provide recommendations in the following JSON format only:
{{
    "products": [
        {{
            "productid": "Product ID",
            "product": "Product Name",
            "reason": "Specific reason for recommending this product based on user profile and behavior"
        }},
    ]
}}

Do not include any additional text or explanations outside of this JSON structure.
Please recommend products that match the user's interests and behavior patterns."""
    
    prompt_filtered = f"""Based on the following user data, suggest personalized product recommendations:

User Profile:
- Name: {user['Name']}
- Email: {user['Email']}
- Age: {user['Age']}
- Location: {user['Location']}
- Gender: {user['Gender']}

Recent Browsing History:
{user_browsing}

Purchase History:
{user_purchases}

IMPORTANT: Provide recommendations in the following JSON format only:
{{
    "products": [
        {{
            "productid": "Product ID",
            "product": "Product Name",
            "reason": "Specific reason for recommending this product based on user profile and behavior"
        }},
    ]
}}

Do not include any additional text or explanations outside of this JSON structure.
Please recommend products that match the user's interests and behavior patterns."""


    try:
        # API call with complete browsing and purchase history
        response_complete = requests.post(
            OPENAI_API_URL,
            headers={
                "api-key": OPENAI_API_KEY,
                "Content-Type": "application/json",
            },
            json={
                "model": "gpt-4o-gs",
                "messages": [
                    {
                        "role": "system",
                        "content": system_prompt_market_trend
                    },
                    {
                        "role": "user",
                        "content": prompt_complete,
                    }
                ],
                "logit_bias": {},
            },
        )

        # API call with filtered browsing and purchase history
        response_filtered = requests.post(
            OPENAI_API_URL,
            headers={
                "api-key": OPENAI_API_KEY,
                "Content-Type": "application/json",
            },
            json={
                "model": "gpt-4o-gs",
                "messages": [
                    {
                        "role": "system",
                        "content": system_prompt_user_history
                    },
                    {
                        "role": "user",
                        "content": prompt_filtered,
                    }
                ],
                "logit_bias": {},
            },
        )

        response_data_complete = response_complete.json()
        response_data_filtered = response_filtered.json()

        if 'choices' not in response_data_complete or not response_data_complete['choices']:
            return {"error": "Invalid response from OpenAI API (complete)"}

        if 'choices' not in response_data_filtered or not response_data_filtered['choices']:
            return {"error": "Invalid response from OpenAI API (filtered)"}

        recommendations_complete_str = response_data_complete['choices'][0]['message']['content']
        recommendations_complete_json = recommendations_complete_str.strip('```json\n').strip('\n```')
        recommendations_complete = json.loads(recommendations_complete_json)

        recommendations_filtered_str = response_data_filtered['choices'][0]['message']['content']
        recommendations_filtered_json = recommendations_filtered_str.strip('```json\n').strip('\n```')
        recommendations_filtered = json.loads(recommendations_filtered_json)

        return {
            "Recommendations based on market trends.": recommendations_complete,
            "Recommendations based on user history": recommendations_filtered
        }

    except Exception as e:
        return {"error": str(e)}