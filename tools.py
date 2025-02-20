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
            {"name": "Red Skirt", "color": "red", "price": 35, "size": "S"},
            {"name": "Blue Jacket", "color": "blue", "price": 80, "size": "M"},
            {"name": "White Shoes", "color": "white", "price": 65, "size": "8"}
        ]
        
        # Mock store prices for comparison
        self.store_prices = {
            "Red Skirt": {"StoreA": 35, "StoreB": 38},
            "Blue Jacket": {"StoreA": 80, "StoreB": 75}
        }

    async def search_products(self, color=None, price=None, size=None):
        """
        Search products with optional filters.
        
        Args:
            color (str, optional): Product color
            price (float, optional): Maximum price
            size (str, optional): Product size
            
        Returns:
            list: Matching products
        """
        results = self.products
        if color:
            results = [p for p in results if p["color"] == color]
        if price:
            results = [p for p in results if p["price"] <= price]
        if size:
            results = [p for p in results if p["size"] == size]
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
