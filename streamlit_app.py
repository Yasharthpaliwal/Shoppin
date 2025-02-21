import streamlit as st
from agents import AgentProcessor
import asyncio
import json

st.title("E-commerce Shopping Assistant")

# Initialize agent
@st.cache_resource
def get_agent():
    return AgentProcessor()

agent = get_agent()

# Create input area
st.write("Try one of our demo queries!")

# Add demo queries as selectable options
demo_queries = [
    "Find a floral skirt under $40 in size S. Is it in stock, and can I apply a discount code 'SAVE10'?",
    "I need white sneakers (size 8) for under $70 that can arrive by Friday.",
    "I found a 'casual denim jacket' at $80 on SiteA. Any better deals?",
    "I want to buy a cocktail dress from SiteB, but only if returns are hassle-free. Do they accept returns?"
]

query = st.selectbox(
    "Select a demo query:",
    [""] + demo_queries,
    index=0,
    placeholder="Choose a query..."
)

# Add a submit button
if st.button("Submit"):
    if query:
        st.write("Processing your query...")
        
        # Create a spinner while processing
        with st.spinner('Thinking...'):
            # Run async code in sync context
            response = asyncio.run(agent.process_query(query))
            
            # Display results in a nice format
            if response["status"] == "success":
                # Display natural language response first
                st.success(response.get("natural_response", "Found what you're looking for!"))
                
                # Display steps taken
                st.write("### 🤔 Steps Taken")
                for step in response["steps"]:
                    with st.expander(f"Step: {step['tool']}"):
                        st.write("**Intent:**", step["reasoning"]["intent"])
                        st.write("**Parameters:**")
                        st.json(step["parameters"])
                        st.write("**Result:**")
                        st.json(step["result"])
                
                # Create an expander for technical details
                with st.expander("See Full Response"):
                    st.json(response)
                    
            else:
                st.error(f"Error: {response['message']}")
    else:
        st.warning("Please select a query!")

# Add description of available tools
with st.expander("Available Tools"):
    st.write("""
    This demo supports the following operations:
    - **Product Search**: Search for products with filters (color, price, size)
    - **Price Comparison**: Compare prices across different stores
    - **Shipping Estimates**: Get shipping cost and delivery time
    - **Discount Calculation**: Calculate prices with promo codes
    - **Return Policy**: Check store return policies
    """)

# Add footer
st.markdown("---")
st.markdown("*E-commerce Shopping Assistant Demo*") 
