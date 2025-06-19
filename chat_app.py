import streamlit as st
from dotenv import load_dotenv
import os
from langchain.agents import initialize_agent, Tool
from langchain_community.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.tools import StructuredTool  # ✅ For multi-input tools
from langchain.agents import AgentType

# Import tools from your tools.py file
from tools import filter_cards_by_income, simulate_reward, filter_cards_advanced

# ✅ Load environment variables (OPENROUTER_API_KEY)
load_dotenv()
api_key = os.getenv("OPENROUTER_API_KEY")

# starting the LLM
llm = ChatOpenAI(
    openai_api_key=api_key,
    base_url="https://openrouter.ai/api/v1",
    model="cohere/command-r-08-2024"  # model used is calude open-ai have paid API tokens
)

# ✅ Setup persistent memory per session
if "memory" not in st.session_state:
    st.session_state.memory = ConversationBufferMemory(memory_key="chat_history")

memory = st.session_state.memory

# ✅ Define tools
tools = [
    Tool(
        name="CardFilterTool",
        func=lambda q: filter_cards_by_income(q),
        description="Filters credit cards based on user's monthly income"
    ),
    StructuredTool.from_function(
        name="CardFilterAdvanced",
        description="Filter cards based on income, reward type, and preferred perks.",
        func=filter_cards_advanced
    ),
    Tool(
        name="RewardSimulator",
        func=lambda q: simulate_reward(q),
        description="Simulates cashback rewards based on monthly income"
    )
]

# Agent for the LangChain

agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent=AgentType.OPENAI_MULTI_FUNCTIONS,  #
    memory=memory,
    verbose=True
)


# UI setup
st.set_page_config(page_title="💳 Credit Card Advisor", layout="centered")
st.title("💳 Credit Card Advisor (AI-Powered)")

# Display chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# User chat input
user_input = st.chat_input("Ask about cards, perks, or simulations...")

if user_input:
    # Display user message
    st.chat_message("user").markdown(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})

    try:
        response = agent.invoke(user_input)

        # If agent returns a dict with "output", extract it
        if isinstance(response, dict) and "output" in response:
            response = response["output"]

        # Format response
        response = str(response).replace("\n", "\n\n")
    except Exception as e:
        response = f"⚠️ Error: {str(e)}"

    # Display assistant response
    st.chat_message("assistant").markdown(response)
    st.session_state.messages.append({"role": "assistant", "content": response})
