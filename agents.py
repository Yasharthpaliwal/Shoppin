from typing import Dict, Any
import tools

class AgentProcessor:
    def __init__(self):
        self.api = tools.MockEcommerceAPI()

    def process_query(self, user_query: str) -> Dict[str, Any]:
        """
        Process user query and return structured response.
        In real implementation, this would use an LLM to extract parameters.
        """
        # Input validation
        if not isinstance(user_query, str):
            return {
                "status": "error",
                "message": "Query must be a string",
                "data": None
            }
        
        if not user_query.strip():
            return {
                "status": "error",
                "message": "Query cannot be empty",
                "data": None
            }

        # Mock LLM parameter extraction
        extracted_params = self._mock_extract_parameters(user_query)
        
        # Handle unknown intent
        if extracted_params["intent"] == "unknown":
            return {
                "status": "error",
                "message": "I couldn't understand your request. Please try rephrasing it.",
                "data": None
            }

        # Route to appropriate handler based on intent
        handlers = {
            "product_search": self._handle_search,
            "price_comparison": self._handle_price_comparison,
            "shipping": self._handle_shipping_estimate,
            "discount": self._handle_discount_check,
            "return_policy": self._handle_return_policy
        }
        
        handler = handlers.get(extracted_params["intent"])
        if not handler:
            return {
                "status": "error",
                "message": "This type of request is not supported",
                "data": None
            }
        
        try:
            return handler(extracted_params["parameters"])
        except Exception as e:
            return {
                "status": "error",
                "message": f"An error occurred while processing your request: {str(e)}",
                "data": None
            }

    def _mock_extract_parameters(self, query: str) -> Dict[str, Any]:
        """
        Mock LLM parameter extraction. In real implementation, 
        this would be replaced with actual LLM call.
        """
        query = query.lower()
        
        # Product Search Intent
        if any(word in query for word in ["find", "search"]):
            return {
                "intent": "product_search",
                "parameters": {
                    "query": query,
                    "color": "red" if "red" in query else (
                        "blue" if "blue" in query else (
                        "white" if "white" in query else None
                    )),
                    "price_range": 40 if "$40" in query else None,
                    "size": "S" if "size s" in query else None
                }
            }
        
        # Price Comparison Intent
        if any(word in query for word in ["compare", "price"]):
            product_name = None
            if "jacket" in query:
                product_name = "Denim Jacket"
            elif "skirt" in query:
                product_name = "Floral Skirt"
            
            return {
                "intent": "price_comparison",
                "parameters": {
                    "product_name": product_name
                }
            }
        
        # Shipping Intent
        if any(word in query for word in ["shipping", "arrive", "delivery"]):
            location = "New York" if "new york" in query else (
                "California" if "california" in query else "unknown"
            )
            return {
                "intent": "shipping",
                "parameters": {
                    "location": location,
                    "delivery_date": "2024-03-01"  # Mock date
                }
            }
        
        # Discount Intent
        if any(word in query for word in ["promo", "discount", "code"]):
            # Extract promo code - assume it's in caps after "code" or "promo"
            words = query.upper().split()
            promo_code = None
            for i, word in enumerate(words):
                if word in ["CODE", "PROMO"]:
                    if i + 1 < len(words):
                        promo_code = words[i + 1]
                        break
                    
            return {
                "intent": "discount",
                "parameters": {
                    "promo_code": promo_code,
                    "base_price": 100  # Mock base price
                }
            }
        
        # Return Policy Intent
        if any(word in query for word in ["return", "returns"]):
            site = None
            if "sitea" in query.lower():
                site = "SiteA"
            elif "siteb" in query.lower():
                site = "SiteB"
            elif "sitec" in query.lower():
                site = "SiteC"
            
            return {
                "intent": "return_policy",
                "parameters": {
                    "site": site or "unknown"
                }
            }
        
        # Unknown Intent
        return {
            "intent": "unknown",
            "parameters": {}
        }

    def _handle_search(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Handle product search with structured response"""
        api_response = self.api.search_products(params)
        return {
            "status": "success",
            "intent": "product_search",
            "data": api_response["data"],
            "metadata": api_response["metadata"]
        }

    def _handle_price_comparison(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Handle price comparison requests"""
        product_name = params.get("product_name", "unknown item")
        response = self.api.compare_prices(product_name)
        return {
            "status": "success",
            "intent": "price_comparison",
            "data": response["data"]
        }

    def _handle_shipping_estimate(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Handle shipping estimate requests"""
        response = self.api.get_shipping_estimate(
            params.get("location", "unknown"),
            params.get("delivery_date", "unknown")
        )
        return {
            "status": "success",
            "intent": "shipping",
            "data": response["data"]
        }

    def _handle_discount_check(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Handle discount code application"""
        response = self.api.check_discount(
            params.get("base_price", 0),
            params.get("promo_code", None)
        )
        return {
            "status": "success",
            "intent": "discount",
            "data": response["data"]
        }

    def _handle_return_policy(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Handle return policy queries"""
        response = self.api.get_return_policy(params.get("site", "unknown"))
        return {
            "status": "success",
            "intent": "return_policy",
            "data": response["data"]
        }

# Example usage
if __name__ == "__main__":
    agent = AgentProcessor()
    test_query = "Find me a red skirt under $40 in size S"
    response = agent.process_query(test_query)
    print(response)
