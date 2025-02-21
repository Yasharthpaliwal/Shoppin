"""
Mock E-commerce API Tools
------------------------
Provides mock implementations of various e-commerce operations
for testing and demonstration purposes.
"""

import random
from typing import Dict, Any, Optional, List
from pydantic import BaseModel



class MockEcommerceAPI:
    """
    Mock implementation of e-commerce API endpoints.
    Simulates product search, price comparison, shipping estimates,
    discount calculations, and return policy queries.
    """

    def __init__(self):
        # Mock product database
        self.products = [
            {"name": "Floral Skirt", "color": "multicolor", "price": 35, "size": "S", "in_stock": True},
            {"name": "White Sneakers", "color": "white", "price": 65, "size": "8", "in_stock": True},
            {"name": "Denim Jacket", "color": "blue", "price": 75, "size": "M", "in_stock": True},
            {"name": "Cocktail Dress", "color": "black", "price": 90, "size": "M", "in_stock": False}
        ]
        
        # Mock store prices for comparison
        self.store_prices = {
            "Floral Skirt": {"StoreA": 35, "StoreB": 38},
            "White Sneakers": {"StoreA": 65, "StoreB": 70},
            "Denim Jacket": {"StoreA": 80, "StoreB": 75, "StoreC": 72}
        }

    async def search_products(self, color=None, price=None, size=None):
        """
        Search products with optional filters.
        
        Args:
            color (str, optional): Product color
            price (float/str, optional): Maximum price
            size (str, optional): Product size
            
        Returns:
            list: Matching products
        """
        results = self.products.copy()
        
        if color:
            results = [p for p in results if p["color"].lower() == color.lower()]
        
        if price is not None:
            try:
                # Convert price to float if it's a string
                max_price = float(str(price).replace('$', '').replace(',', ''))
                results = [p for p in results if p["price"] <= max_price]
            except (ValueError, TypeError):
                print(f"Invalid price value: {price}")
        
        if size:
            results = [p for p in results if p["size"].lower() == str(size).lower()]
        
        return results

    async def compare_prices(self, product_name):
        """Compare prices across stores"""
        return self.store_prices.get(product_name, {})

    async def get_shipping(self, location):
        """Get shipping estimate"""
        return {
            "cost": random.randint(5, 20),
            "days": random.randint(3, 7)
        }

    async def check_discount(self, promo_code, price):
        """Check discount"""
        discounts = {"SAVE10": 0.1, "SAVE20": 0.2}
        discount = discounts.get(promo_code, 0)
        return {
            "original": price,
            "discount": discount,
            "final": price * (1 - discount)
        }

    async def get_return_policy(self, store_name):
        """Get store return policy"""
        policies = {
            "StoreA": "30-day returns",
            "StoreB": "14-day returns"
        }
        return policies.get(store_name, "Policy not found")

if __name__ == "__main__":
    # Test cases
    api = MockEcommerceAPI()
    
    # Test product search
    print(api.search_products(color="red", price=40, size="S"))
    
    # Test shipping estimate
    print(api.get_shipping("New York"))
    
    # Test discount
    print(api.check_discount("SAVE10", 100))
    
    # Test price comparison
    print(api.compare_prices("Blue Jacket"))
    
    # Test return policy
    print(api.get_return_policy("StoreB"))
