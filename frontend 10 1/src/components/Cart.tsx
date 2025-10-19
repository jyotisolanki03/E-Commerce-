import React from 'react';
import { ShoppingCart, Trash2 } from 'lucide-react';
import { useCart } from '../context/CartContext';

export const Cart: React.FC = () => {
  const { state, dispatch } = useCart();

  const updateQuantity = (productId: string, quantity: number) => {
    if (quantity < 1) return;
    dispatch({ type: 'UPDATE_QUANTITY', payload: { productId, quantity } });
  };

  if (state.items.length === 0) {
    return (
      <div className="text-center py-8">
        <ShoppingCart className="mx-auto w-16 h-16 text-gray-400" />
        <p className="mt-4 text-gray-600">Your cart is empty</p>
      </div>
    );
  }

  return (
    <div className="bg-white rounded-lg shadow p-6">
      <h2 className="text-2xl font-bold mb-4">Shopping Cart</h2>
      {state.items.map((item) => (
        <div key={item.product.id} className="flex items-center py-4 border-b">
          <img
            src={item.product.image}
            alt={item.product.name}
            className="w-20 h-20 object-cover rounded"
          />
          <div className="ml-4 flex-grow">
            <h3 className="font-semibold">{item.product.name}</h3>
            <p className="text-gray-600">${item.product.price.toFixed(2)}</p>
            <div className="flex items-center mt-2">
              <button
                onClick={() => updateQuantity(item.product.id, item.quantity - 1)}
                className="px-2 py-1 bg-gray-100 rounded-l"
              >
                -
              </button>
              <span className="px-4 py-1 bg-gray-50">{item.quantity}</span>
              <button
                onClick={() => updateQuantity(item.product.id, item.quantity + 1)}
                className="px-2 py-1 bg-gray-100 rounded-r"
              >
                +
              </button>
            </div>
          </div>
          <button
            onClick={() => dispatch({ type: 'REMOVE_FROM_CART', payload: item.product.id })}
            className="ml-4 text-red-500 hover:text-red-700"
          >
            <Trash2 className="w-5 h-5" />
          </button>
        </div>
      ))}
      <div className="mt-6">
        <div className="flex justify-between text-xl font-bold">
          <span>Total:</span>
          <span>${state.total.toFixed(2)}</span>
        </div>
        <button
          onClick={() => dispatch({ type: 'CLEAR_CART' })}
          className="mt-4 w-full bg-blue-600 text-white py-2 px-4 rounded hover:bg-blue-700"
        >
          Checkout
        </button>
      </div>
    </div>
  );
};