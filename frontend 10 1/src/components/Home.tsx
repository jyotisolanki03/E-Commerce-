import React, { useEffect, useState } from 'react';
import { ProductCard } from './ProductCard';
import { products } from '../data/mockData';
import { Product } from '../types';
import { Loader2 } from 'lucide-react';

export const Home: React.FC = () => {
  const [loading, setLoading] = useState(true);
  const [recommendedProducts, setRecommendedProducts] = useState<Product[]>([]);
  const [trendingProducts, setTrendingProducts] = useState<Product[]>([]);

  useEffect(() => {
    const loadRecommendations = () => {
      const recommendationsData = localStorage.getItem('userRecommendations');
      
      if (recommendationsData) {
        const recommendations = JSON.parse(recommendationsData);
        
        // Get trending products
        const trendingProductIds = recommendations['Recommendations based on market trends.'].products
          .map((item: any) => item.productid);
        const trending = products.filter(product => 
          trendingProductIds.includes(product.id)
        );
        
        // Get recommended products
        const recommendedProductIds = recommendations['Recommendations based on user history'].products
          .map((item: any) => item.productid);
        const recommended = products.filter(product => 
          recommendedProductIds.includes(product.id)
        );
        
        setTrendingProducts(trending);
        setRecommendedProducts(recommended);
      } else {
        // Fallback to default products if no recommendations
        setTrendingProducts(products.slice(0, 3));
        setRecommendedProducts(products.slice(3, 6));
      }
      
      setLoading(false);
    };

    loadRecommendations();
  }, []);

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-[50vh]">
        <Loader2 className="w-8 h-8 animate-spin text-blue-600" />
        <span className="ml-2 text-gray-600">Loading recommendations...</span>
      </div>
    );
  }

  return (
    <div className="space-y-12">
      <section>
        <div className="flex justify-between items-center mb-6">
          <h2 className="text-2xl font-bold text-gray-900">Recommended for You</h2>
        </div>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {recommendedProducts.map((product) => (
            <ProductCard key={product.id} product={product} />
          ))}
        </div>
      </section>

      <section>
        <div className="flex justify-between items-center mb-6">
          <h2 className="text-2xl font-bold text-gray-900">Trending Now</h2>
        </div>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {trendingProducts.map((product) => (
            <ProductCard key={product.id} product={product} />
          ))}
        </div>
      </section>

      <section className="bg-blue-50 rounded-2xl p-8">
        <div className="max-w-3xl mx-auto text-center">
          <h2 className="text-2xl font-bold text-gray-900 mb-4">
            Shop with Confidence
          </h2>
          <p className="text-gray-600 mb-8">
            Enjoy free shipping, 30-day returns, and our price match guarantee.
          </p>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div className="p-4">
              <div className="text-blue-600 font-bold mb-2">Free Shipping</div>
              <p className="text-gray-600 text-sm">On orders over $50</p>
            </div>
            <div className="p-4">
              <div className="text-blue-600 font-bold mb-2">30-Day Returns</div>
              <p className="text-gray-600 text-sm">Hassle-free returns</p>
            </div>
            <div className="p-4">
              <div className="text-blue-600 font-bold mb-2">Secure Payment</div>
              <p className="text-gray-600 text-sm">100% secure checkout</p>
            </div>
          </div>
        </div>
      </section>
    </div>
  );
};