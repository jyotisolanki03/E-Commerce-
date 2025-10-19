import requests
import json
from config import OPENAI_API_KEY, OPENAI_API_URL
from models import products, users, browsing_history, purchase_history, cart_activity
import asyncio
import aiohttp
from datetime import datetime, timedelta

    


def call_openai(prompt):
    try:
        response = requests.post(
            'https://maqopenai.openai.azure.com/openai/deployments/gpt-35-turbo-16k/chat/completions?api-version=2024-05-01-preview',
            headers={
                "api-key": "9ef17db85cdd4dc7aef8a23c7945f89a",
                "Content-Type": "application/json",
            },
            json={
                "model": "gpt-35-turbo-16k",
                "messages": [
                    {
                        "role": "system",
                        "content": """Objective:
Given the following NoSQL database for Orders and Inventory, identify the product IDs and user IDs for orders that can be delayed. The delay occurs if shipping the order causes the product to go out of stock in the inventory for the specified delivery city or if there is bad weather at the delivery location that may cause a delay.
Instructions:
1. **Process Orders Chronologically**:
   - Process the orders in chronological order based on the `Timestamp` field to ensure the correct sequence of operations.
2. **Inventory Check**:
   - For each order, check the inventory for the specific `DeliveryCity` to determine if the product is in stock.
   - For each product in the order, verify if the quantity in the inventory is sufficient to fulfill the order.
   - If the inventory quantity is insufficient, mark the product as delayed.
   - As you process each order, decrease the quantity of the ordered product in the inventory for that location.
3. **Weather Check**:
   - For each order, check the weather forecast for the specific `DeliveryCity`.
   - If the weather is bad (Only rainy weather, rest all weather is good), mark the product as delayed due to weather conditions.
    - Incase the weather is fine (Sunny/Clear or any other weather except rainy), the product is not delayed.
    - Don't hallucinate any reason. Give correct reason only. If out of stock, mention out of stock. If bad weather, mention bad weather. If no delay, dont return it.
   4. **Output Format**:
   - Return the delayed `ProductID`, `UserID`, `OrderID`, and `Reason` for delay in a structured format with NO PREAMBLE.
Example: [
    {
      "OrderID": "O001",
      "UserID": "U001",
      "ProductID": "P025",
      "Reason": "Out of Stock"
    },
    {
      "OrderID": "O003",
      "UserID": "U002",
      "ProductID": "P014",
      "Reason": "Bad Weather"
    },
    ...
]
Note: Strictly if there is no Product ID in an inventory, consider it as out of stock.
Note: Dont hallucinate any reason. Give correct reason only. If out of stock, mention out of stock. If bad weather, mention bad weather. If no delay, dont return it.
Note: Strictly return me the output array only. No need to give other details. Just return the array output as specified.
"""
                    },
                    {
                        "role": "user",
                        "content": prompt,
                    }
                ],
                "logit_bias": {},
            },
        )

        response_data = response.json()
        return response_data['choices'][0]['message']['content']

    except Exception as e:
        return {"error": str(e)}

def call_openai_cart(prompt):
    try:
        response = requests.post(
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
                        "content": """
                        You are an email marketing specialist for a premium e-commerce platform. Create abandoned cart recovery emails following this strict format:

FORMAT RULES:
1. Subject Line: Clean, with 1-2 emojis maximum
2. Body: EXACTLY two parts:
   - One cohesive paragraph (no line breaks)
   - One final call-to-action line (separated by a single \\n)
3. NO greetings (no "Hi", "Hello", etc.)
4. NO sign-offs (no "Best regards", "Thanks", etc.)
5. NO bullet points
6. NO multiple paragraphs

Example Format:
{
  "userId": "U001",
  "subject": "Complete Your Premium Collection ✨",
  "body": "Your carefully selected Product X represents the perfect blend of style and functionality, offering outstanding quality and timeless appeal. This exclusive piece combines premium materials with expert craftsmanship, ensuring an exceptional addition to your collection at $X.\\n\\nSecure your Product X now - limited stock available."
}

Keep the tone professional yet engaging, focusing on value proposition rather than urgency. Emphasize product quality and benefits in a sophisticated manner.
"""
                    },
                    {
                        "role": "user",
                        "content": prompt,
                    }
                ],
                "logit_bias": {},
            },
        )

        response_data = response.json()
        return response_data['choices'][0]['message']['content']

    except Exception as e:
        return {"error": str(e)}

    

def identify_abandoned_carts():
    """
    Identify carts that have been inactive for more than 24 hours.
    """
    abandoned_carts = []
    current_time = datetime.utcnow()
    # print(f"Current time: {current_time}")  # Debugging purpose
    
    for cart in cart_activity:
        last_activity = datetime.strptime(cart["LastActivity"], "%Y-%m-%dT%H:%M:%SZ")
        # print(f"CartID: {cart['CartID']}, LastActivity: {last_activity}")  # Debugging purpose
        if (current_time - last_activity) > timedelta(hours=24):
            abandoned_carts.append(cart)
    
    return abandoned_carts

def call_openai_reviews(prompt):
    try:
        response = requests.post(
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
                        "content": """
                        You are a helpful AI assistant that analyzes product reviews and creates insightful, balanced summaries to help shoppers make informed decisions.
"""
                    },
                    {
                        "role": "user",
                        "content": prompt,
                    }
                ],
                "logit_bias": {},
            },
        )

        response_data = response.json()
        return response_data['choices'][0]['message']['content']

    except Exception as e:
        return {"error": str(e)}