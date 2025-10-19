import pandas as pd
import json
from datetime import datetime
import logging
from typing import Dict, List, Any
from nixtla import NixtlaClient
import requests
import numpy as np

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize NixtlaClient
NIXTLA_API_KEY = "nixak-jJXpogOgadaJ7L6v2ziBku9rp6nt9UwOHNWRv4Sf4Y2cZDOXyeuj8VtxtyM9RtGzNESdOzhHU4xUwOvj"
nixtla_client = NixtlaClient(api_key=NIXTLA_API_KEY) if NIXTLA_API_KEY else None
if not nixtla_client:
    logger.error("NIXTLA_API_KEY environment variable not set.")

# OpenAI API configuration
OPENAI_API_KEY = "3e03bd5e1ee3439189c5f0b3d186dcff"
OPENAI_API_URL = "https://maq-openai.openai.azure.com/openai/deployments/gpt-4o-gs/chat/completions?api-version=2024-05-01-preview"

SAFETY_STOCK_FACTOR = 1.2
STOCKOUT_THRESHOLD = 0.8

SYSTEM_PROMPT = """
You are an expert inventory analyst. Given product data, a sales forecast, and lead time, 
calculate the following:

1.  **Stockout Probability:** Determine the likelihood of a stockout based on current stock, predicted sales, and a safety stock factor.
2.  **Days Until Stockout:** Calculate how many days the current stock will last given the sales forecast.
3.  **Reorder Recommendation:** Decide if a reorder is needed based on the stockout probability and reorder threshold. 
4.  **Reorder Quantity:** If a reorder is needed, calculate the quantity needed to maintain safety stock
5.  **Reorder Urgency:** Define if the reorder is urgent based on the stockout probability and lead time.
6.  **Reasoning:** Provide clear explanation for all the above calculation and decisions.It should be clear,concise and focused on helping the user understand the analysis.

Return the results in JSON format with the following keys:

*   `stockout_probability` (float): Probability of stockout
*   `days_until_stockout` (int): Number of days until stockout
*   `reorder` (bool): True if a reorder is needed, False otherwise.
*   `quantity` (int): Reorder quantity (0 if no reorder).
*   `urgency` (string): "low", "medium", or "high".
*   `reasoning` (string): Explanation of the analysis.
Note: do not include any additional text or explanations outside of this JSON structure.Avoid any unnecessary details and provide only the required information.Avoid Generic phrases in the response/summary.
"""


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


if __name__ == '__main__':
    # Example usage
    inventory_list = [
  {
    "InventoryID": "I001",
    "DeliveryCity": "New York",
    "NumberOfPartners": 2,
    "ProductList": [
      {
        "ProductID": "P001",
        "Quantity": 150,
        "ReorderQuantity": 100,
        "LeadTimeDays": 7,
        "WeeklySales": {
          "2024-01-01": 20,
          "2024-01-08": 25,
          "2024-01-15": 30,
          "2024-01-22": 35,
          "2024-01-29": 28,
          "2024-02-05": 32,
          "2024-02-12": 40
        }
      },
      {
        "ProductID": "P002",
        "Quantity": 75,
        "ReorderQuantity": 50,
        "LeadTimeDays": 10,
        "WeeklySales": {
          "2024-01-01": 10,
          "2024-01-08": 15,
          "2024-01-15": 12,
          "2024-01-22": 18,
          "2024-01-29": 16,
          "2024-02-05": 20,
          "2024-02-12": 22
        }
      },
      {
          "ProductID": "P003",
          "Quantity": 110,
          "ReorderQuantity": 80,
          "LeadTimeDays": 5,
          "WeeklySales": {
            "2024-01-01": 15,
            "2024-01-08": 18,
            "2024-01-15": 22,
            "2024-01-22": 20,
            "2024-01-29": 25,
            "2024-02-05": 28,
            "2024-02-12": 23
          }
      }
    ]
  },
  {
    "InventoryID": "I002",
    "DeliveryCity": "Mumbai",
    "NumberOfPartners": 3,
    "ProductList": [
      { "ProductID": "P014", "Quantity": 10, "ReorderQuantity": 15, "LeadTimeDays": 3,
        "WeeklySales": {
            "2024-01-01": 2,
            "2024-01-08": 3,
            "2024-01-15": 2,
            "2024-01-22": 4,
            "2024-01-29": 3,
            "2024-02-05": 4,
            "2024-02-12": 5
          }},
      { "ProductID": "P018", "Quantity": 7, "ReorderQuantity": 10, "LeadTimeDays": 5,
          "WeeklySales": {
            "2024-01-01": 1,
            "2024-01-08": 2,
            "2024-01-15": 3,
            "2024-01-22": 2,
            "2024-01-29": 1,
            "2024-02-05": 3,
            "2024-02-12": 2
          }},
      { "ProductID": "P005", "Quantity": 6, "ReorderQuantity": 8, "LeadTimeDays": 2,
           "WeeklySales": {
            "2024-01-01": 3,
            "2024-01-08": 4,
            "2024-01-15": 2,
            "2024-01-22": 4,
            "2024-01-29": 5,
            "2024-02-05": 2,
            "2024-02-12": 3
          }},
      { "ProductID": "P002", "Quantity": 4, "ReorderQuantity": 6, "LeadTimeDays": 4,
          "WeeklySales": {
            "2024-01-01": 2,
            "2024-01-08": 1,
            "2024-01-15": 3,
            "2024-01-22": 2,
            "2024-01-29": 1,
            "2024-02-05": 2,
            "2024-02-12": 3
        }},
      { "ProductID": "P007", "Quantity": 2, "ReorderQuantity": 4, "LeadTimeDays": 3,
          "WeeklySales": {
            "2024-01-01": 1,
            "2024-01-08": 0,
            "2024-01-15": 2,
            "2024-01-22": 1,
            "2024-01-29": 2,
            "2024-02-05": 1,
            "2024-02-12": 0
        }},
      { "ProductID": "P009", "Quantity": 3, "ReorderQuantity": 5, "LeadTimeDays": 2,
         "WeeklySales": {
            "2024-01-01": 2,
            "2024-01-08": 2,
            "2024-01-15": 1,
            "2024-01-22": 1,
            "2024-01-29": 3,
            "2024-02-05": 2,
            "2024-02-12": 1
        } },
      { "ProductID": "P012", "Quantity": 5, "ReorderQuantity": 7, "LeadTimeDays": 4,
         "WeeklySales": {
            "2024-01-01": 1,
            "2024-01-08": 3,
            "2024-01-15": 2,
            "2024-01-22": 3,
            "2024-01-29": 1,
            "2024-02-05": 2,
            "2024-02-12": 3
        }}
    ]
  },
  {
    "InventoryID": "I003",
    "DeliveryCity": "London",
    "NumberOfPartners": 4,
    "ProductList": [
      {
        "ProductID": "P021",
        "Quantity": 120,
        "ReorderQuantity": 90,
        "LeadTimeDays": 6,
        "WeeklySales": {
            "2024-01-01": 22,
            "2024-01-08": 28,
            "2024-01-15": 30,
            "2024-01-22": 25,
            "2024-01-29": 33,
             "2024-02-05": 36,
            "2024-02-12": 32
        }
      },
        {
        "ProductID": "P025",
        "Quantity": 85,
        "ReorderQuantity": 60,
        "LeadTimeDays": 8,
          "WeeklySales": {
              "2024-01-01": 18,
              "2024-01-08": 20,
              "2024-01-15": 24,
              "2024-01-22": 21,
              "2024-01-29": 26,
               "2024-02-05": 27,
              "2024-02-12": 25
          }
      },
     { "ProductID": "P008", "Quantity": 9, "ReorderQuantity": 12, "LeadTimeDays": 3,
        "WeeklySales": {
            "2024-01-01": 3,
            "2024-01-08": 4,
            "2024-01-15": 2,
            "2024-01-22": 4,
            "2024-01-29": 3,
            "2024-02-05": 5,
            "2024-02-12": 4
        } },
      { "ProductID": "P028", "Quantity": 3, "ReorderQuantity": 5, "LeadTimeDays": 6,
       "WeeklySales": {
            "2024-01-01": 1,
            "2024-01-08": 2,
            "2024-01-15": 1,
            "2024-01-22": 3,
            "2024-01-29": 2,
            "2024-02-05": 1,
            "2024-02-12": 2
        } }
    ]
  },
    {
    "InventoryID": "I004",
    "DeliveryCity": "Tokyo",
    "NumberOfPartners": 5,
     "ProductList": [
      {
        "ProductID": "P006",
        "Quantity": 95,
          "ReorderQuantity": 70,
        "LeadTimeDays": 9,
        "WeeklySales": {
             "2024-01-01": 12,
              "2024-01-08": 15,
              "2024-01-15": 18,
             "2024-01-22": 16,
              "2024-01-29": 19,
            "2024-02-05": 21,
              "2024-02-12": 20
           }
      },
       {
         "ProductID": "P029",
        "Quantity": 30,
           "ReorderQuantity": 20,
          "LeadTimeDays": 12,
          "WeeklySales": {
              "2024-01-01": 7,
               "2024-01-08": 9,
             "2024-01-15": 8,
              "2024-01-22": 11,
              "2024-01-29": 10,
               "2024-02-05": 13,
              "2024-02-12": 12
          }
      },
        { "ProductID": "P011", "Quantity": 1, "ReorderQuantity": 2, "LeadTimeDays": 10,
         "WeeklySales": {
            "2024-01-01": 0,
            "2024-01-08": 1,
            "2024-01-15": 0,
            "2024-01-22": 1,
            "2024-01-29": 0,
            "2024-02-05": 1,
            "2024-02-12": 0
         }},
        { "ProductID": "P017", "Quantity": 5, "ReorderQuantity": 8, "LeadTimeDays": 6,
          "WeeklySales": {
            "2024-01-01": 2,
            "2024-01-08": 1,
            "2024-01-15": 3,
            "2024-01-22": 2,
            "2024-01-29": 3,
            "2024-02-05": 1,
            "2024-02-12": 2
        }},
        { "ProductID": "P020", "Quantity": 2, "ReorderQuantity": 3, "LeadTimeDays": 7,
          "WeeklySales": {
            "2024-01-01": 0,
            "2024-01-08": 2,
            "2024-01-15": 1,
            "2024-01-22": 2,
            "2024-01-29": 0,
            "2024-02-05": 1,
            "2024-02-12": 0
        } }
    ]
  },
  {
    "InventoryID": "I005",
    "DeliveryCity": "Sydney",
    "NumberOfPartners": 2,
    "ProductList": [
        {
            "ProductID":"P030",
            "Quantity": 150,
              "ReorderQuantity": 110,
            "LeadTimeDays": 7,
             "WeeklySales": {
                "2024-01-01": 18,
                 "2024-01-08": 22,
                "2024-01-15": 25,
                 "2024-01-22": 20,
               "2024-01-29": 23,
                "2024-02-05": 26,
                "2024-02-12": 24
              }
          },
      {
        "ProductID": "P027",
         "Quantity": 10,
          "ReorderQuantity": 10,
          "LeadTimeDays": 8,
          "WeeklySales": {
            "2024-01-01": 5,
              "2024-01-08": 6,
            "2024-01-15": 7,
             "2024-01-22": 4,
              "2024-01-29": 7,
              "2024-02-05": 8,
             "2024-02-12": 9
        }
      },
      { "ProductID": "P004", "Quantity": 15, "ReorderQuantity": 20, "LeadTimeDays": 2,
           "WeeklySales": {
              "2024-01-01": 3,
               "2024-01-08": 4,
              "2024-01-15": 2,
               "2024-01-22": 3,
                "2024-01-29": 4,
                 "2024-02-05": 2,
                "2024-02-12": 5
        } },
      { "ProductID": "P010", "Quantity": 6, "ReorderQuantity": 8, "LeadTimeDays": 4,
          "WeeklySales": {
            "2024-01-01": 1,
            "2024-01-08": 2,
            "2024-01-15": 3,
            "2024-01-22": 2,
            "2024-01-29": 1,
            "2024-02-05": 2,
            "2024-02-12": 3
        }},
      { "ProductID": "P013", "Quantity": 3, "ReorderQuantity": 5, "LeadTimeDays": 3,
           "WeeklySales": {
            "2024-01-01": 2,
             "2024-01-08": 1,
           "2024-01-15": 2,
            "2024-01-22": 3,
            "2024-01-29": 1,
             "2024-02-05": 2,
            "2024-02-12": 1
        }},
      { "ProductID": "P015", "Quantity": 10, "ReorderQuantity": 12, "LeadTimeDays": 5,
       "WeeklySales": {
            "2024-01-01": 3,
            "2024-01-08": 2,
            "2024-01-15": 4,
            "2024-01-22": 1,
            "2024-01-29": 3,
            "2024-02-05": 2,
            "2024-02-12": 4
        } }
    ]
  }
]

    # Analyze entire inventory
    # analysis_result = analyze_inventory_data(inventory_list)
    # print("Inventory Analysis Result:")
    # print(json.dumps(analysis_result, indent=4))
    # print("\n")

    # Get product specific forecast
    product_id = 'P001'
    product_forecast = get_product_forecast_data(inventory_list, product_id)
    print(f"Product Forecast for {product_id}:")
    print(json.dumps(product_forecast, indent=4))