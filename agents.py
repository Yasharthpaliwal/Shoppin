"""
E-commerce Agent System
----------------------
This system implements a ReAct pattern to process natural language queries 
for e-commerce operations using LLM for tool selection and parameter extraction.

Author: [Yasharth Singh Paliwal]
Date: [20]
"""

from typing import Dict, Any
import openai
import json
import os
import tools
from openai import AzureOpenAI
import streamlit as st
from dotenv import load_dotenv


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
        
        # Azure OpenAI Configuration
        self.client = AzureOpenAI(
            api_key=api_key=os.getenv("AZURE_API_KEY"),
            azure_endpoint=os.getenv("AZURE_ENDPOINT"),
            api_version=os.getenv("AZURE_API_VERSION")
        )
        
        self.deployment_name = "gpt-35-turbo"
        
        # Available tools configuration
        self.available_tools = {
            "search_products": ["color", "price", "size"],
            "compare_prices": ["product_name"],
            "get_shipping": ["location"],
            "check_discount": ["promo_code", "price"],
            "get_return_policy": ["store_name"]
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
                - tool: Tool used
                - parameters: Extracted parameters
                - result: API response
                
        Example:
            Input: "Find red shoes under $50"
            Output: {
                "status": "success",
                "query": "Find red shoes under $50",
                "tool": "search_products",
                "parameters": {"color": "red", "price": 50},
                "result": [...]
            }
        """
        if not query.strip():
            return {"status": "error", "message": "Empty query"}

        try:
            # Get tool selection and parameters from LLM
            tool_response = await self._get_tool_and_params(query)
            if isinstance(tool_response, str):
                tool_response = json.loads(tool_response)
                
            tool_name = tool_response.get("tool")
            params = tool_response.get("parameters", {})

            # Validate tool existence
            if tool_name not in self.available_tools:
                return {"error": "Tool not found"}

            # Execute selected tool
            api_method = getattr(self.api, tool_name)
            api_result = await api_method(**params)

            # Return structured response
            return {
                "status": "success",
                "query": query,
                "tool": tool_name,
                "parameters": params,
                "result": api_result
            }

        except Exception as e:
            return {"status": "error", "message": str(e)}

    async def _get_tool_and_params(self, query: str) -> Dict[str, Any]:
        """Use LLM to identify tool and extract parameters"""
        try:
            prompt = f"""
            Given these available tools and their parameters:
            {self.available_tools}

            For the query: "{query}"
            
            Return
            
                "tool": "tool_name",
                "parameters": 
                "param1": "value1",
                "param2: "Value"

            "reasoning": "Explain why this tool was chosen."
            Note: For price parameters, always return numeric values without currency symbols.
            """

            response = self.client.chat.completions.create(
                model=self.deployment_name,
                messages=[
                    {"role": "system", "content": prompt},
                    {"role": "user", "content": query}
                ],
                temperature=0
            )
            
            # Parse the response and ensure price is float
            content = json.loads(response.choices[0].message.content)
            if 'parameters' in content and 'price' in content['parameters']:
                content['parameters']['price'] = float(str(content['parameters']['price']).replace('$', ''))
            
            return content
            
        except Exception as e:
            raise Exception(f"Azure OpenAI API error: {str(e)}")

