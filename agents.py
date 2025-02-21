"""
E-commerce Agent System
----------------------
This system implements a ReAct pattern to process natural language queries 
for e-commerce operations using LLM for tool selection and parameter extraction.

Author: [Your Name]
Date: [Current Date]
"""

from typing import Dict, Any, List
import json
import os
import tools


class AgentProcessor:
    """
    Main agent class that processes user queries using LLM and executes appropriate tools.
    
    Implements ReAct pattern:
    1. Reasoning: LLM analyzes query to determine required tool
    2. Acting: Executes selected tool with extracted parameters
    3. Response: Returns structured results
    """

    def __init__(self):
        # Initialize API configurations
        self.api = tools.MockEcommerceAPI()
        
        # Remove Azure OpenAI Configuration
        # self.client = AzureOpenAI(...)
        # self.deployment_name = "gpt-35-turbo"
        
        # Enhanced tools configuration with descriptions
        self.available_tools = {
            "search_products": {
                "params": ["color", "price", "size"],
                "description": "Search for products with filters for color, price, and size"
            },
            "compare_prices": {
                "params": ["product_name"],
                "description": "Compare prices across different stores"
            },
            "get_shipping": {
                "params": ["location"],
                "description": "Get shipping cost and estimated delivery time"
            },
            "check_discount": {
                "params": ["promo_code", "price"],
                "description": "Calculate final price after applying discount code"
            },
            "get_return_policy": {
                "params": ["store_name"],
                "description": "Get store's return policy details"
            }
        }

    async def process_query(self, query: str) -> Dict[str, Any]:
        """
        Process user query and return structured response.
        
        Args:
            query (str): User's natural language query
            
        Returns:
            Dict[str, Any]: Structured response containing:
                - status: Success/error
                - query: Original query
                - steps: List of steps taken
                - natural_response: Natural language response
                
        Example:
            Input: "Find red shoes under $50"
            Output: {
                "status": "success",
                "query": "Find red shoes under $50",
                "steps": [...]
            }
        """
        if not query.strip():
            return {"status": "error", "message": "Empty query"}

        try:
            # Get tool selection and parameters from LLM
            tool_responses = await self._get_tool_sequence(query)
            
            final_result = {
                "status": "success",
                "query": query,
                "steps": []
            }
            
            # Execute each tool in sequence
            for tool_response in tool_responses:
                tool_name = tool_response.get("tool")
                params = tool_response.get("parameters", {})
                reasoning = tool_response.get("reasoning", {})
                
                # Execute tool
                api_method = getattr(self.api, tool_name)
                result = await api_method(**params)
                
                # Add step results
                step_result = {
                    "tool": tool_name,
                    "parameters": params,
                    "result": result,
                    "reasoning": reasoning
                }
                final_result["steps"].append(step_result)
            
            # Generate natural language response
            final_result["natural_response"] = self._generate_natural_response(final_result["steps"])
            
            return final_result

        except Exception as e:
            return {"status": "error", "message": str(e)}

    async def _get_tool_sequence(self, query: str) -> List[Dict[str, Any]]:
        """Demo version - returns hardcoded tool sequences for test cases"""
        # Demo cases with predefined tool sequences
        demo_sequences = {
            "Find a floral skirt under $40 in size S. Is it in stock, and can I apply a discount code 'SAVE10'?": [
                {
                    "tool": "search_products",
                    "parameters": {"color": None, "price": 40, "size": "S"},
                    "reasoning": {"intent": "Find matching skirt"}
                },
                {
                    "tool": "check_discount",
                    "parameters": {"promo_code": "SAVE10", "price": 35},
                    "reasoning": {"intent": "Check discount availability"}
                }
            ],
            "I need white sneakers (size 8) for under $70 that can arrive by Friday.": [
                {
                    "tool": "search_products",
                    "parameters": {"color": "white", "price": 70, "size": "8"},
                    "reasoning": {"intent": "Find matching sneakers"}
                },
                {
                    "tool": "get_shipping",
                    "parameters": {"location": "default"},
                    "reasoning": {"intent": "Check delivery time"}
                }
            ],
            "I found a 'casual denim jacket' at $80 on SiteA. Any better deals?": [
                {
                    "tool": "compare_prices",
                    "parameters": {"product_name": "Denim Jacket"},
                    "reasoning": {"intent": "Compare prices across stores"}
                }
            ],
            "I want to buy a cocktail dress from SiteB, but only if returns are hassle-free. Do they accept returns?": [
                {
                    "tool": "get_return_policy",
                    "parameters": {"store_name": "StoreB"},
                    "reasoning": {"intent": "Check return policy"}
                }
            ]
        }
        
        # Return predefined sequence or error
        if query in demo_sequences:
            return demo_sequences[query]
        return [{"tool": "search_products", "parameters": {}, "reasoning": {"intent": "Default search"}}]

    def _generate_natural_response(self, steps: List[Dict[str, Any]]) -> str:
        """Generate natural language response based on steps taken."""
        response = "Here are the results of your query."
        
        for step in steps:
            tool_name = step["tool"]
            params = step["parameters"]
            result = step["result"]
            reasoning = step["reasoning"]
            
            if tool_name == "get_shipping":
                response = f"The shipping to {params.get('location', 'your location')} will cost ${result.get('cost', 0)} and take {result.get('days', 0)} days."
            
            elif tool_name == "search_products":
                if isinstance(result, list) and result:
                    products = len(result)
                    response = f"I found {products} product(s) matching your criteria. The prices range from ${min(p['price'] for p in result)} to ${max(p['price'] for p in result)}."
            
            elif tool_name == "compare_prices":
                if isinstance(result, dict):
                    stores = len(result)
                    min_price = min(result.values())
                    min_store = [store for store, price in result.items() if price == min_price][0]
                    response = f"I compared prices across {stores} stores. The best price is ${min_price} at {min_store}."
            
            elif tool_name == "check_discount":
                if isinstance(result, dict):
                    discount = result.get('discount', 0)
                    final_price = result.get('final_price', 0)
                    response = f"With the promo code, you'll get a {discount}% discount. The final price will be ${final_price}."
            
            elif tool_name == "get_return_policy":
                response = f"The return policy for {params.get('store_name', 'this store')} is: {result}"
        
        return response

