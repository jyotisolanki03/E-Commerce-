import React, { useState } from 'react';
import { Package, TrendingUp, AlertTriangle, CheckCircle2, XCircle } from 'lucide-react';
import { products } from '../data/mockData';
import { Product } from '../types';

interface ForecastData {
  product_id: string;
  current_stock: number;
  forecast: {
    next_7_days: {
      predicted_sales: number;
      daily_predictions: number[];
      stockout_probability: number;
    };
    recommended_actions: {
      stockout_probability: number;
      days_until_stockout: number;
      reorder: boolean;
      quantity: number;
      urgency: string;
      reasoning: string;
    };
  };
}

export const AdminPortal: React.FC = () => {
  const [selectedProduct, setSelectedProduct] = useState<Product | null>(null);
  const [forecastData, setForecastData] = useState<ForecastData | null>(null);
  const [loading, setLoading] = useState(false);
  const [showDialog, setShowDialog] = useState(false);

  const handleProductClick = async (product: Product) => {
    setSelectedProduct(product);
    setLoading(true);
    setShowDialog(true);

    try {
      const response = await fetch('http://127.0.0.1:5000/forecast', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ ProductID: product.id }),
      });

      if (!response.ok) {
        throw new Error('Failed to fetch forecast data');
      }

      const data = await response.json();
      setForecastData(data);
    } catch (error) {
      console.error('Error fetching forecast:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 p-8">
      <div className="max-w-7xl mx-auto">
        <div className="flex items-center justify-between mb-8">
          <div className="flex items-center space-x-3">
            <Package className="w-8 h-8 text-blue-600" />
            <h1 className="text-2xl font-bold text-gray-900">Admin Portal</h1>
          </div>
          <div className="flex items-center space-x-2 bg-blue-50 px-4 py-2 rounded-lg">
            <TrendingUp className="w-5 h-5 text-blue-600" />
            <span className="text-blue-700 font-medium">Stock Forecasting</span>
          </div>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
          {products.map((product) => (
            <div
              key={product.id}
              onClick={() => handleProductClick(product)}
              className="bg-white rounded-lg shadow-sm border border-gray-200 overflow-hidden hover:shadow-md transition-shadow cursor-pointer"
            >
              <img
                src={product.image}
                alt={product.name}
                className="w-full h-48 object-cover"
                onError={(e) => {
                  e.currentTarget.src = 'https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=800';
                }}
              />
              <div className="p-4">
                <h3 className="font-semibold text-gray-900 mb-2">{product.name}</h3>
                <div className="flex justify-between items-center">
                  <span className="text-sm text-gray-600">Stock: {product.stock}</span>
                  <span className="text-sm font-medium text-blue-600">${product.price.toFixed(2)}</span>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Forecast Dialog */}
      {showDialog && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4">
          <div className="bg-white rounded-lg shadow-xl max-w-2xl w-full max-h-[90vh] overflow-y-auto">
            <div className="p-6">
              <div className="flex justify-between items-start mb-6">
                <h2 className="text-xl font-bold text-gray-900">
                  {selectedProduct?.name} - Forecast Analysis
                </h2>
                <button
                  onClick={() => setShowDialog(false)}
                  className="text-gray-400 hover:text-gray-500"
                >
                  <XCircle className="w-6 h-6" />
                </button>
              </div>

              {loading ? (
                <div className="flex items-center justify-center py-12">
                  <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600" />
                </div>
              ) : forecastData ? (
                <div className="space-y-6">
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <div className="bg-blue-50 p-4 rounded-lg">
                      <h3 className="font-semibold text-blue-900 mb-2">Current Stock</h3>
                      <p className="text-2xl font-bold text-blue-700">
                        {forecastData.current_stock} units
                      </p>
                    </div>
                    <div className="bg-orange-50 p-4 rounded-lg">
                      <h3 className="font-semibold text-orange-900 mb-2">Predicted Sales (7 days)</h3>
                      <p className="text-2xl font-bold text-orange-700">
                        {forecastData.forecast.next_7_days.predicted_sales.toFixed(2)} units
                      </p>
                    </div>
                  </div>

                  <div className="border-t pt-4">
                    <h3 className="font-semibold text-gray-900 mb-4">Daily Sales Predictions</h3>
                    <div className="grid grid-cols-7 gap-2">
                      {forecastData.forecast.next_7_days.daily_predictions.map((prediction, index) => (
                        <div key={index} className="text-center">
                          <div className="text-sm text-gray-600">Day {index + 1}</div>
                          <div className="font-medium">{prediction.toFixed(1)}</div>
                        </div>
                      ))}
                    </div>
                  </div>

                  <div className="bg-gray-50 p-4 rounded-lg">
                    <div className="flex items-start space-x-3">
                      {forecastData.forecast.recommended_actions.urgency === 'high' ? (
                        <AlertTriangle className="w-5 h-5 text-red-500 flex-shrink-0 mt-1" />
                      ) : (
                        <CheckCircle2 className="w-5 h-5 text-green-500 flex-shrink-0 mt-1" />
                      )}
                      <div>
                        <h3 className="font-semibold text-gray-900 mb-2">Recommended Actions</h3>
                        <p className="text-gray-700 text-sm">
                          {forecastData.forecast.recommended_actions.reasoning}
                        </p>
                      </div>
                    </div>
                  </div>

                  <div className="grid grid-cols-2 gap-4">
                    <div className="bg-gray-50 p-4 rounded-lg">
                      <h4 className="text-sm font-medium text-gray-700">Days Until Stockout</h4>
                      <p className="text-xl font-bold text-gray-900">
                        {forecastData.forecast.recommended_actions.days_until_stockout} days
                      </p>
                    </div>
                    <div className="bg-gray-50 p-4 rounded-lg">
                      <h4 className="text-sm font-medium text-gray-700">Recommended Reorder</h4>
                      <p className="text-xl font-bold text-gray-900">
                        {forecastData.forecast.recommended_actions.quantity} units
                      </p>
                    </div>
                  </div>
                </div>
              ) : (
                <div className="text-center py-12 text-gray-500">
                  Failed to load forecast data
                </div>
              )}
            </div>
          </div>
        </div>
      )}
    </div>
  );
};