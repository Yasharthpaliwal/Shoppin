import random
from typing import Dict, Any, Optional, List

class MockEcommerceAPI:
    def __init__(self):
        self.mock_products = [
            {"name": "Floral Skirt", "color": "red", "price": 35, "size": "S", "stock": True},
            {"name": "Denim Jacket", "color": "blue", "price": 80, "size": "M", "stock": True},
            {"name": "White Sneakers", "color": "white", "price": 65, "size": "8", "stock": False},
        ]
        
        self.mock_prices = {
            "Denim Jacket": {"SiteA": 80, "SiteB": 75, "SiteC": 78},
            "Floral Skirt": {"SiteA": 40, "SiteB": 35, "SiteC": 38},
        }
        
        self.mock_policies = {
            "SiteA": "30-day return policy with free shipping.",
            "SiteB": "No returns on sale items. 14-day return period.",
            "SiteC": "Full refund within 7 days, exchange within 30 days.",
        }
        
        self.valid_promo_codes = {
            "SAVE10": 10,
            "FASHION20": 20
        }

    def search_products(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Search products with filters
        """
        results = []
        for product in self.mock_products:
            if self._matches_criteria(product, params):
                results.append(product)
                
        return {
            "status": "success",
            "data": results,
            "metadata": {
                "total_results": len(results),
                "filters_applied": params
            }
        }

    def _matches_criteria(self, product: Dict[str, Any], params: Dict[str, Any]) -> bool:
        """Helper method to check if product matches search criteria"""
        color = params.get('color')
        price_range = params.get('price_range')
        size = params.get('size')
        
        return (
            (not color or product['color'] == color) and
            (not price_range or product['price'] <= price_range) and
            (not size or product['size'] == size)
        )

    def get_shipping_estimate(self, location: str, delivery_date: str) -> Dict[str, Any]:
        """
        Estimate shipping details
        """
        return {
            "status": "success",
            "data": {
                "cost": random.randint(5, 20),
                "estimated_delivery": delivery_date,
                "feasible": True,
                "location": location
            }
        }

    def check_discount(self, base_price: float, promo_code: str) -> Dict[str, Any]:
        """
        Validate and apply discount
        """
        discount = self.valid_promo_codes.get(promo_code, 0)
        final_price = base_price * (1 - discount / 100)
        
        return {
            "status": "success",
            "data": {
                "final_price": round(final_price, 2),
                "discount_applied": discount > 0,
                "discount_percentage": discount
            }
        }

    def compare_prices(self, product_name: str) -> Dict[str, Any]:
        """
        Compare prices across different stores
        """
        prices = self.mock_prices.get(product_name)
        return {
            "status": "success",
            "data": prices if prices else "No competitor prices found."
        }

    def get_return_policy(self, site_name: str) -> Dict[str, Any]:
        """
        Get return policy for a specific site
        """
        policy = self.mock_policies.get(site_name)
        return {
            "status": "success",
            "data": policy if policy else "No return policy available."
        }

if __name__ == "__main__":
    # Test cases
    api = MockEcommerceAPI()
    
    # Test product search
    print(api.search_products({"color": "red", "price_range": 40, "size": "S"}))
    
    # Test shipping estimate
    print(api.get_shipping_estimate("New York", "2025-02-22"))
    
    # Test discount
    print(api.check_discount(100, "SAVE10"))
    
    # Test price comparison
    print(api.compare_prices("Denim Jacket"))
    
    # Test return policy
    print(api.get_return_policy("SiteB"))
