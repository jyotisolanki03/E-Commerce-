import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import { Star, ShoppingCart, ThumbsUp, MessageSquare, Plus, Minus, Loader2, ArrowRight } from 'lucide-react';
import { Product } from '../types';
import { useCart } from '../context/CartContext';
import { generateAIReviewSummary } from '../utils/reviewUtils';
import { products } from '../data/mockData';

interface SimilarProduct {
  Brand: string;
  Category: string;
  Name: string;
  Price: number;
  ProductID: string;
  Tags: string[];
  Title: string;
}

interface ReviewSummaryResponse {
  product_name: string;
  review_count: number;
  similar_products: SimilarProduct[];
  summary: string;
}

export const ProductDetails: React.FC = () => {
  const { id } = useParams();
  const product = products.find(p => p.id === id);
  const { dispatch } = useCart();
  const [aiSummary, setAiSummary] = useState<string>('');
  const [pros, setPros] = useState<string[]>([]);
  const [cons, setCons] = useState<string[]>([]);
  const [isLoadingSummary, setIsLoadingSummary] = useState(true);
  const [similarProducts, setSimilarProducts] = useState<SimilarProduct[]>([]);

  useEffect(() => {
    const fetchSummary = async () => {
      try {
        const response = await fetch('http://127.0.0.1:5000/product-review-summary', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ product_id: id }),
        });
        const data: ReviewSummaryResponse = await response.json();
        
        // Extract main summary (everything before Pros)
        const mainSummary = data.summary.split('**Pros:**')[0].trim();
        setAiSummary(mainSummary);

        // Updated regex patterns to match the exact format
        const prosSection = data.summary.split('**Pros:**')[1]?.split('**Cons:**')[0];
        const consSection = data.summary.split('**Cons:**')[1];

        if (prosSection) {
          const prosList = prosSection
            .split('\n')
            .filter(item => item.trim().startsWith('•'))
            .map(item => item.trim().replace('• ', ''));
          setPros(prosList);
        }

        if (consSection) {
          const consList = consSection
            .split('\n')
            .filter(item => item.trim().startsWith('•'))
            .map(item => item.trim().replace('• ', ''));
          setCons(consList);
        }

        // Set similar products
        setSimilarProducts(data.similar_products);
      } catch (error) {
        console.error('Error fetching summary:', error);
      } finally {
        setIsLoadingSummary(false);
      }
    };

    if (id) {
      fetchSummary();
    }
  }, [id]);

  if (!product) {
    return (
      <div className="text-center py-12">
        <h2 className="text-2xl font-bold text-gray-900">Product not found</h2>
        <p className="mt-2 text-gray-600">The product you're looking for doesn't exist.</p>
      </div>
    );
  }

  const reviewSummary = {
    averageRating: product.rating,
    totalReviews: product.reviews.length,
    ratingDistribution: product.reviews.reduce((acc, review) => {
      acc[review.rating] = (acc[review.rating] || 0) + 1;
      return acc;
    }, {} as Record<number, number>),
  };

  return (
    <div className="max-w-7xl mx-auto">
      <div className="grid grid-cols-1 md:grid-cols-2 gap-12">
        <div className="relative">
          <img
            src={product.image}
            alt={product.name}
            className="w-full rounded-2xl shadow-lg object-cover"
          />
          {product.stock === 0 && (
            <div className="absolute top-4 right-4 bg-red-500 text-white px-4 py-2 rounded-full text-sm font-medium">
              Out of Stock
            </div>
          )}
        </div>

        <div className="space-y-6">
          <div>
            <h1 className="text-3xl font-bold text-gray-900 mb-2">{product.name}</h1>
            <p className="text-gray-600">{product.description}</p>
          </div>

          <div className="flex items-center space-x-4">
            <div className="flex items-center">
              <Star className="w-5 h-5 text-yellow-400 fill-current" />
              <span className="ml-2 font-semibold">{product.rating}</span>
            </div>
            <span className="text-gray-400">|</span>
            <span className="text-gray-600">
              {product.reviews.length} reviews
            </span>
          </div>

          <div className="text-3xl font-bold text-gray-900">
            ${product.price.toFixed(2)}
          </div>

          {product.isDelayed && (
            <div className="bg-red-50 border border-red-200 rounded-lg p-4">
              <p className="text-red-700 font-medium">
                Shipping Delayed
              </p>
              <p className="text-red-600 text-sm mt-1">
                Due to {product.delayReason === 'stock' ? 'stock availability' : 'weather conditions'}
              </p>
            </div>
          )}

          <button
            onClick={() => dispatch({ type: 'ADD_TO_CART', payload: product })}
            disabled={product.stock === 0}
            className={`w-full flex items-center justify-center space-x-2 py-3 px-8 rounded-lg ${
              product.stock === 0
                ? 'bg-gray-200 cursor-not-allowed'
                : 'bg-blue-600 hover:bg-blue-700 text-white'
            }`}
          >
            <ShoppingCart className="w-5 h-5" />
            <span>{product.stock === 0 ? 'Out of Stock' : 'Add to Cart'}</span>
          </button>
        </div>
      </div>

      <div className="mt-16 space-y-12">
        <section>
          <h2 className="text-2xl font-bold text-gray-900 mb-6">AI Review Summary</h2>
          {isLoadingSummary ? (
            <div className="flex items-center justify-center p-8">
              <Loader2 className="w-6 h-6 text-blue-600 animate-spin" />
            </div>
          ) : (
            <>
              <div className="bg-gradient-to-r from-blue-50 to-indigo-50 rounded-lg p-6 border border-blue-100 mb-8">
                <div className="flex items-start space-x-4">
                  <div className="flex-shrink-0">
                    <MessageSquare className="w-6 h-6 text-blue-600" />
                  </div>
                  <div>
                    <p className="text-gray-800 leading-relaxed">{aiSummary}</p>
                  </div>
                </div>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                {/* Pros Section */}
                <div className="bg-green-50 rounded-lg p-6 border border-green-100">
                  <div className="flex items-center space-x-2 mb-4">
                    <Plus className="w-5 h-5 text-green-600" />
                    <h3 className="text-lg font-semibold text-green-800">Pros</h3>
                  </div>
                  <ul className="space-y-3">
                    {pros.map((pro, index) => (
                      <li key={index} className="flex items-start space-x-2">
                        <span className="w-1.5 h-1.5 rounded-full bg-green-500 mt-2" />
                        <span className="text-gray-700">{pro}</span>
                      </li>
                    ))}
                  </ul>
                </div>

                {/* Cons Section */}
                <div className="bg-red-50 rounded-lg p-6 border border-red-100">
                  <div className="flex items-center space-x-2 mb-4">
                    <Minus className="w-5 h-5 text-red-600" />
                    <h3 className="text-lg font-semibold text-red-800">Cons</h3>
                  </div>
                  <ul className="space-y-3">
                    {cons.map((con, index) => (
                      <li key={index} className="flex items-start space-x-2">
                        <span className="w-1.5 h-1.5 rounded-full bg-red-500 mt-2" />
                        <span className="text-gray-700">{con}</span>
                      </li>
                    ))}
                  </ul>
                </div>
              </div>
            </>
          )}
        </section>

        <section>
          <h2 className="text-2xl font-bold text-gray-900 mb-6">Customer Reviews</h2>
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
            <div className="lg:col-span-1">
              <div className="bg-white rounded-lg shadow-sm p-6 border border-gray-200">
                <div className="text-center">
                  <div className="text-5xl font-bold text-gray-900 mb-2">
                    {reviewSummary.averageRating.toFixed(1)}
                  </div>
                  <div className="flex items-center justify-center mb-4">
                    {Array.from({ length: 5 }).map((_, i) => (
                      <Star
                        key={i}
                        className={`w-5 h-5 ${
                          i < Math.floor(reviewSummary.averageRating)
                            ? 'text-yellow-400 fill-current'
                            : 'text-gray-300'
                        }`}
                      />
                    ))}
                  </div>
                  <p className="text-gray-600">
                    Based on {reviewSummary.totalReviews} reviews
                  </p>
                </div>

                <div className="mt-6 space-y-2">
                  {[5, 4, 3, 2, 1].map((rating) => (
                    <div key={rating} className="flex items-center">
                      <span className="w-12 text-sm text-gray-600">
                        {rating} stars
                      </span>
                      <div className="flex-grow mx-4 h-2 bg-gray-200 rounded-full overflow-hidden">
                        <div
                          className="h-full bg-yellow-400"
                          style={{
                            width: `${
                              ((reviewSummary.ratingDistribution[rating] || 0) /
                                reviewSummary.totalReviews) *
                              100
                            }%`,
                          }}
                        />
                      </div>
                      <span className="w-12 text-right text-sm text-gray-600">
                        {reviewSummary.ratingDistribution[rating] || 0}
                      </span>
                    </div>
                  ))}
                </div>
              </div>
            </div>

            <div className="lg:col-span-2 space-y-6">
              {product.reviews.map((review) => (
                <div
                  key={review.id}
                  className="bg-white rounded-lg shadow-sm p-6 border border-gray-200"
                >
                  <div className="flex items-center justify-between mb-4">
                    <div className="flex items-center space-x-4">
                      <div className="flex items-center">
                        {Array.from({ length: 5 }).map((_, i) => (
                          <Star
                            key={i}
                            className={`w-4 h-4 ${
                              i < review.rating
                                ? 'text-yellow-400 fill-current'
                                : 'text-gray-300'
                            }`}
                          />
                        ))}
                      </div>
                      <span className="font-medium text-gray-900">
                        {review.userName}
                      </span>
                    </div>
                    <span className="text-sm text-gray-500">
                      {new Date(review.date).toLocaleDateString()}
                    </span>
                  </div>
                  <p className="text-gray-700">{review.comment}</p>
                  <div className="mt-4 flex items-center space-x-4">
                    <button className="flex items-center space-x-2 text-gray-500 hover:text-gray-700">
                      <ThumbsUp className="w-4 h-4" />
                      <span className="text-sm">Helpful</span>
                    </button>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </section>

        {/* Similar Products Section */}
        {similarProducts.length > 0 && (
          <section className="mt-16">
            <div className="flex items-center justify-between mb-8">
              <h2 className="text-2xl font-bold text-gray-900">Similar Products</h2>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-3 lg:grid-cols-4 gap-6">
              {similarProducts.map((product) => {
                // Find the product image from mockData
                const mockProduct = products.find(p => p.id === product.ProductID);
                
                return (
                  <div
                    key={product.ProductID}
                    className="bg-white rounded-xl shadow-sm hover:shadow-md transition-all duration-200 overflow-hidden group"
                  >
                    {/* Product Image from mockData */}
                    <div className="aspect-square relative overflow-hidden bg-gray-100">
                      <img
                        src={mockProduct?.image || `https://source.unsplash.com/400x400/?${encodeURIComponent(product.Category)}`}
                        alt={product.Name}
                        className="object-cover w-full h-full group-hover:scale-105 transition-transform duration-300"
                      />
                    </div>

                    {/* Product Details */}
                    <div className="p-4">
                      <div className="mb-1">
                        <span className="text-sm text-blue-600 font-medium">
                          {product.Brand}
                        </span>
                      </div>
                      <h3 className="font-medium text-gray-900 group-hover:text-blue-600 transition-colors duration-200 mb-2 truncate">
                        {product.Name}
                      </h3>
                      <div className="flex items-center justify-between">
                        <span className="text-lg font-bold text-gray-900">
                          ${product.Price.toFixed(2)}
                        </span>
                        <button
                          onClick={() => {
                            window.location.href = `/product/${product.ProductID}`;
                          }}
                          className="bg-blue-600 text-white px-3 py-1.5 rounded-lg text-sm font-medium hover:bg-blue-700 transition-colors duration-200"
                        >
                          View
                        </button>
                      </div>  
                    </div>
                  </div>
                );
              })}
            </div>
          </section>
        )}
      </div>
    </div>
  );
};