import pandas as pd
import json
from datetime import datetime
import logging
from typing import Dict, List, Any
from nixtla import NixtlaClient
import requests
import numpy as np
from prompt import SYSTEM_PROMPT
from config import NIXTLA_API_KEY, OPENAI_API_KEY, OPENAI_API_URL
# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize NixtlaClient

nixtla_client = NixtlaClient(api_key=NIXTLA_API_KEY) if NIXTLA_API_KEY else None
if not nixtla_client:
    logger.error("NIXTLA_API_KEY environment variable not set.")

# OpenAI API configuration
SAFETY_STOCK_FACTOR = 1.2
STOCKOUT_THRESHOLD = 0.8

def prepare_timeseries_data(product_data: Dict[str, Any]) -> pd.DataFrame:
    """Convert product sales data into TimeGPT compatible format"""
    df = pd.DataFrame(list(product_data['WeeklySales'].items()), columns=['timestamp', 'value'])
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df['value'] = pd.to_numeric(df['value'])
    return df.sort_values('timestamp')


def generate_forecast(product_data: Dict[str, Any]) -> Dict[str, Any] | None:
    """Generate forecast using TimeGPT and get recommendations from LLM"""
    if not nixtla_client:
        logger.error("Nixtla client not initialized. Cannot generate forecast.")
        return None
    try:
        ts_df = prepare_timeseries_data(product_data)
        forecast_df = nixtla_client.forecast(df=ts_df, h=7, time_col='timestamp', target_col='value')

        total_predicted_sales = forecast_df['TimeGPT'].sum()
        current_stock = int(product_data['Quantity'])
        daily_predictions = forecast_df['TimeGPT'].tolist()

        # Prepare the LLM prompt
        prompt = f"""
            Product ID: {product_data['ProductID']}
            Current Stock: {current_stock}
            Predicted Sales (Next 7 Days): {total_predicted_sales}
            Daily Sales Predictions (Next 7 Days): {daily_predictions}
            Reorder Quantity: {product_data['ReorderQuantity']}
            Lead Time Days: {product_data['LeadTimeDays']}
            Safety Stock Factor: {SAFETY_STOCK_FACTOR}
            Stockout Threshold: {STOCKOUT_THRESHOLD}
        """

        llm_response = call_llm(prompt)
        if llm_response:
           return {
            'product_id': product_data['ProductID'],
            'current_stock': current_stock,
            'forecast': {
                'next_7_days': {
                    'predicted_sales': total_predicted_sales,
                    'daily_predictions': daily_predictions,
                    'stockout_probability': llm_response.get('stockout_probability')
                },
                'recommended_actions': llm_response
            }
            }
        else:
             return None
            
    except Exception as e:
        logger.error(f"Error generating forecast for product {product_data['ProductID']}: {str(e)}")
        return None


def call_llm(prompt: str) -> Dict[str, Any] | None:
    """Calls the OpenAI API with the given prompt and returns the JSON response."""
    try:
        response = requests.post(
            OPENAI_API_URL,
            headers={
                "api-key": OPENAI_API_KEY,
                "Content-Type": "application/json",
            },
            json={
                "model": "gpt-4o-gs", # Or choose a suitable model name
                "messages": [
                    {
                        "role": "system",
                        "content": SYSTEM_PROMPT,
                    },
                    {
                        "role": "user",
                        "content": prompt,
                    }
                ],
                "response_format": { "type": "json_object" } # To ensure json response.
            },
        )

        response.raise_for_status()  # Raise an exception for non-200 status codes
        response_data = response.json()

        if response_data and response_data.get('choices'):
            try:
                json_content = response_data['choices'][0]['message']['content']
                return json.loads(json_content)
            except json.JSONDecodeError:
                logger.error(f"LLM response content is not a valid json: {json_content}")
                return None
        else:
            logger.error(f"LLM response is invalid: {response_data}")
            return None
    
    except requests.exceptions.RequestException as e:
        logger.error(f"Error during LLM API call: {e}")
        return None
    

def analyze_inventory(inventory_data: Dict[str, Any]) -> Dict[str, Any]:
    """Analyze a single inventory and generate recommendations"""
    results = [forecast for product in inventory_data['ProductList'] if (forecast := generate_forecast(product))]
    return {
        'inventory_id': inventory_data['InventoryID'],
        'delivery_city': inventory_data['DeliveryCity'],
        'analysis_timestamp': datetime.now().isoformat(),
        'product_forecasts': results
    }


def analyze_inventory_data(inventory_list: List[Dict[str, Any]]):
    """Analyzes a list of inventory data and returns the analysis for each."""
    all_results = []
    for inventory_data in inventory_list:
        try:
            analysis_result = analyze_inventory(inventory_data)
            all_results.append(analysis_result)
        except Exception as e:
            logger.error(f"Error processing inventory analysis: {str(e)}")
            all_results.append({'error': str(e), 'inventory_id': inventory_data.get('InventoryID', 'N/A')})
    return all_results


def get_product_forecast_data(inventory_list: List[Dict[str, Any]], product_id):
    """Gets the forecast for a specific product across all inventories."""
    for inventory_data in inventory_list:
        for product in inventory_data.get('ProductList', []):
            if product['ProductID'] == product_id:
                try:
                    return generate_forecast(product)
                except Exception as e:
                    logger.error(f"Error generating product forecast for {product_id}: {str(e)}")
                    return {'error': str(e)}
    return {'error': 'Product not found'}


    # Example usage
    
    # Analyze entire inventory
    # analysis_result = analyze_inventory_data(inventory_list)
    # print("Inventory Analysis Result:")
    # print(json.dumps(analysis_result, indent=4))
    # print("\n")

    # Get product specific forecast
    # product_id = 'P001'
    # product_forecast = get_product_forecast_data(inventory_list, product_id)
    # print(f"Product Forecast for {product_id}:")
    # print(json.dumps(product_forecast, indent=4))