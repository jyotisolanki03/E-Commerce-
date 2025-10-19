import React from 'react';
import { Star } from 'lucide-react';
import { Product } from '../types';
import { useCart } from '../context/CartContext';
import { Link } from 'react-router-dom';

interface ProductCardProps {
  product: Product;
}

export const ProductCard: React.FC<ProductCardProps> = ({ product }) => {
  const { dispatch } = useCart();

  return (
    <div className="bg-white rounded-lg shadow-md overflow-hidden">
      <Link to={`/product/${product.id}`}>
        <img 
          src={product.image} 
          alt={product.name} 
          className="w-full h-48 object-cover"
        />
      </Link>
      <div className="p-4">
        <Link to={`/product/${product.id}`}>
          <h3 className="text-lg font-semibold mb-2">{product.name}</h3>
        </Link>
        <div className="flex items-center mb-2">
          <Star className="w-4 h-4 text-yellow-400 fill-current" />
          <span className="ml-1">{product.rating}</span>
        </div>
        <p className="text-gray-600 mb-2">${product.price.toFixed(2)}</p>
        <button
          onClick={() => dispatch({ type: 'ADD_TO_CART', payload: product })}
          className={`w-full py-2 px-4 rounded bg-blue-600 hover:bg-blue-700 text-white`}
        >
          Add to Cart
        </button>
      </div>
    </div>
  );
};