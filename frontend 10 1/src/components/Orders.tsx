import React, { useEffect, useState } from 'react';
import { Clock, AlertTriangle, Package, Loader2 } from 'lucide-react';
import { products } from '../data/mockData';
import { useAuth } from '../context/AuthContext';

interface OrderIssue {
  OrderID: string;
  ProductID: string;
  Reason: string;
  UserID: string;
}

interface OnTimeOrder {
  OrderID: string;
  ProductID: string;
  UserID: string;
}

interface OrdersResponse {
  issues: OrderIssue[];
  on_time_orders: OnTimeOrder[];
}

export const Orders: React.FC = () => {
  const [isLoading, setIsLoading] = useState(true);
  const [orders, setOrders] = useState<OrdersResponse | null>(null);
  const { user } = useAuth();

  useEffect(() => {
    const fetchOrders = async () => {
      if (!user?.email) {
        console.error('No user email found');
        setIsLoading(false);
        return;
      }

      try {
        const response = await fetch('http://127.0.0.1:5000/issue', {
          headers: {
            'email': user.email,
          },
        });
        const data = await response.json();
        setOrders(data);
      } catch (error) {
        console.error('Error fetching orders:', error);
      } finally {
        setIsLoading(false);
      }
    };

    fetchOrders();
  }, []); // Empty dependency array ensures it only runs once

  if (isLoading) {
    return (
      <div className="flex items-center justify-center min-h-[60vh]">
        <Loader2 className="w-8 h-8 text-blue-600 animate-spin" />
      </div>
    );
  }

  const delayedProducts = orders?.issues.map(issue => ({
    ...products.find(p => p.id === issue.ProductID),
    orderId: issue.OrderID,
    reason: issue.Reason,
  })).filter(Boolean) || [];

  const onTimeProducts = orders?.on_time_orders.map(order => ({
    ...products.find(p => p.id === order.ProductID),
    orderId: order.OrderID,
  })).filter(Boolean) || [];

  return (
    <div className="space-y-8">
      <div className="border-b pb-4">
        <h1 className="text-2xl font-bold text-gray-900">Your Orders</h1>
      </div>

      {delayedProducts.length > 0 && (
        <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-4 mb-6">
          <div className="flex items-start">
            <AlertTriangle className="w-5 h-5 text-yellow-600 mt-0.5 mr-3" />
            <div>
              <h3 className="text-sm font-medium text-yellow-800">
                Shipping Delays Notice
              </h3>
              <p className="mt-1 text-sm text-yellow-700">
                Some items in your orders are experiencing delays. We appreciate your patience.
              </p>
            </div>
          </div>
        </div>
      )}

      {/* Delayed Orders */}
      {delayedProducts.length > 0 && (
        <div className="space-y-4">
          <h2 className="text-lg font-semibold text-red-600 flex items-center gap-2">
            <Clock className="w-5 h-5" />
            Delayed Orders
          </h2>
          <div className="space-y-4">
            {delayedProducts.map((item: any) => (
              <div
                key={item.orderId}
                className="bg-white rounded-lg shadow-sm border border-red-100 overflow-hidden hover:shadow-md transition-shadow"
              >
                <div className="p-6">
                  <div className="flex items-center justify-between mb-4">
                    <div className="flex items-center space-x-4">
                      <img
                        src={item.image}
                        alt={item.name}
                        className="w-16 h-16 object-cover rounded-lg"
                      />
                      <div>
                        <h3 className="text-lg font-medium text-gray-900">
                          {item.name}
                        </h3>
                        <p className="text-sm text-gray-500">
                          Order #{item.orderId}
                        </p>
                      </div>
                    </div>
                    <div className="text-right">
                      <span className="text-lg font-medium text-gray-900">
                        ${item.price.toFixed(2)}
                      </span>
                    </div>
                  </div>

                  <div className="border-t pt-4">
                    <div className="flex items-center space-x-2 text-red-600">
                      <Clock className="w-4 h-4" />
                      <span className="text-sm font-medium">
                        Delayed due to {item.reason}
                      </span>
                    </div>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* On-time Orders */}
      {onTimeProducts.length > 0 && (
        <div className="space-y-4">
          <h2 className="text-lg font-semibold text-green-600 flex items-center gap-2">
            <Package className="w-5 h-5" />
            On-time Orders
          </h2>
          <div className="space-y-4">
            {onTimeProducts.map((item: any) => (
              <div
                key={item.orderId}
                className="bg-white rounded-lg shadow-sm border border-green-100 overflow-hidden hover:shadow-md transition-shadow"
              >
                <div className="p-6">
                  <div className="flex items-center justify-between">
                    <div className="flex items-center space-x-4">
                      <img
                        src={item.image}
                        alt={item.name}
                        className="w-16 h-16 object-cover rounded-lg"
                      />
                      <div>
                        <h3 className="text-lg font-medium text-gray-900">
                          {item.name}
                        </h3>
                        <p className="text-sm text-gray-500">
                          Order #{item.orderId}
                        </p>
                      </div>
                    </div>
                    <div className="text-right">
                      <span className="text-lg font-medium text-gray-900">
                        ${item.price.toFixed(2)}
                      </span>
                    </div>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};