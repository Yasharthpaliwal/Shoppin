import streamlit as st
from agents import AgentProcessor
import asyncio

st.title("E-commerce Shopping Assistant")

# Initialize agent
@st.cache_resource
def get_agent():
    return AgentProcessor()

agent = get_agent()

# Create input area
st.write("Ask me anything about products, prices, shipping, or returns!")
query = st.text_input("Your Query:", placeholder="Example: Find me a red skirt under $40")

# Add a submit button
if st.button("Submit"):
    if query:
        st.write("Processing your query...")
        
        # Create a spinner while processing
        with st.spinner('Thinking...'):
            # Run async code in sync context
            response = asyncio.run(agent.process_query(query))
            
            # Display results in a nice format
            st.write("### Results:")
            if response["status"] == "success":
                st.success("Found what you're looking for!")
                
                # Display tool used
                st.write(f"🔧 Tool Used: {response['tool']}")
                
                # Display parameters
                st.write("📋 Parameters:")
                for param, value in response['parameters'].items():
                    st.write(f"- {param}: {value}")
                
                # Display results
                st.write("🎯 Results:")
                if isinstance(response['result'], list):
                    for item in response['result']:
                        st.write("---")
                        for key, value in item.items():
                            st.write(f"{key}: {value}")
                else:
                    st.json(response['result'])
            else:
                st.error(f"Error: {response['message']}")
    else:
        st.warning("Please enter a query!")

# Add some helpful examples
with st.expander("Example Queries"):
    st.write("""
    Try these queries:
    - Find me a red skirt under $40
    - Compare prices for Blue Jacket
    - What's the shipping cost to New York?
    - Check discount with code SAVE10
    - What's the return policy for StoreA?
    """)

# Add footer
st.markdown("---")
st.markdown("*Powered by Azure OpenAI and ReAct Pattern*") 