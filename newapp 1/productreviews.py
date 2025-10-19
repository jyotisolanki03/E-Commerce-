import json
from flask import Flask, request, jsonify
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

import requests
import json
from config import OPENAI_API_KEY, OPENAI_API_URL
from models import products, users, browsing_history, purchase_history, cart_activity
import asyncio
import aiohttp
from datetime import datetime, timedelta


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
def create_review_prompt(product_name: str, reviews: List[Dict]) -> str:
    """
    Creates a well-structured prompt for the OpenAI API based on product reviews.
    """
    # Format reviews into a clean text representation
    formatted_reviews = "\n".join([
        f"Review {i+1}:\n"
        f"Rating: {review.get('rating', 'N/A')}/5\n"
        f"Date: {review.get('date', 'N/A')}\n"
        f"Comment: {review.get('comment', 'N/A')}\n"
        for i, review in enumerate(reviews)
    ])
    
    prompt = f"""
Product: {product_name}

Reviews:
{formatted_reviews}

Based on the above reviews for {product_name}, provide a concise and focused summary that:  
1. Highlights the most common positive points  
2. Notes consistent concerns or issues raised by reviewers  
3. Identifies any patterns or trends in customer experiences  

The summary should:  
- Be concise, to the point, and free of unnecessary details  
- Strictly avoid generic phrases or repetitive language  
- Remain natural, easy to read, and helpful for potential buyers  

After the summary, provide a "Pros and Cons" section formatted as follows:  

**Pros:**  
• [First key advantage]  
• [Second key advantage]  
• [Third key advantage]  

**Cons:**  
• [First main drawback]  
• [Second main drawback]  

Ensure the summary and "Pros and Cons" sections are clear, concise, and focused on helping buyers make informed decisions. Avoid generic phrases at the beginning of responses and emphasize identifiable patterns in the reviews.
"""
    return prompt



def get_similar_products(products: List[Dict], 
                        input_product_id: str,
                        n_recommendations: int = 2,
                        different_brand: bool = False,
                        text_weight: float = 0.7,
                        price_weight: float = 0.3) -> List[Dict]:
    """
    Find similar products based on text similarity and price.
    
    Args:
        products: List of product dictionaries
        input_product_id: ID of the product to find similarities for
        n_recommendations: Number of recommendations to return
        different_brand: If True, excludes products from the same brand
        text_weight: Weight for text similarity (0 to 1)
        price_weight: Weight for price similarity (0 to 1)
    
    Returns:
        List of similar product dictionaries
    """
    # Initialize the model
    model = SentenceTransformer('paraphrase-MiniLM-L6-v2')
    
    # Find input product
    input_product = next(p for p in products if p['ProductID'] == input_product_id)
    
    # Prepare text features for all products
    text_features = []
    for product in products:
        text = f"{product['Title']} {product['Category']} {' '.join(product['Tags'])}"
        text_features.append(text)
    
    # Get embeddings
    embeddings = model.encode(text_features)
    
    # Calculate text similarity
    text_similarities = cosine_similarity([embeddings[products.index(input_product)]], embeddings)[0]
    
    # Combine similarities
    combined_similarities = (text_weight * text_similarities)
    
    # Create list of (index, similarity) tuples
    product_similarities = list(enumerate(combined_similarities))
    
    # Filter out same brand if requested
    if different_brand:
        product_similarities = [
            (idx, sim) for idx, sim in product_similarities
            if products[idx]['Brand'] != input_product['Brand']
        ]
    
    # Sort by similarity and get top N (excluding the input product)
    product_similarities.sort(key=lambda x: x[1], reverse=True)
    similar_indices = [idx for idx, _ in product_similarities if products[idx] != input_product][:n_recommendations]
    
    return [products[idx] for idx in similar_indices]
