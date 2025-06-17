import streamlit as st
from langchain.agents import initialize_agent, Tool
from langchain_community.llms import OpenAI
from langchain.memory import ConversationBufferMemory
from tools import filter_cards_by_income, simulate_reward, filter_cards_advanced
from dotenv import load_dotenv
import os

# Load OpenAI key
load_dotenv()
api_key = os.getenv("k-proj--bUk4kEJeBgR2viiQ1a6mMWnYoiP7ZLf7H_Ry9Ff4mIh-tsxQe5QAJTtB_NfHCxRJuhQAmfQx5T3BlbkFJ0IxCfSKHTGxx9cY0EEsNSpQ-xkma14Gkrg70qqnsKd4S_Euvukm5YGeDVzX9mW8ZKAMSu3rsMA")

# Set up LLM
llm = OpenAI(openai_api_key=api_key, temperature=0)

# Define tools
tools = [
    Tool(
        name="CardFilterTool",
        func=lambda q: filter_cards_by_income(q),
        description="Filters credit cards based on user's monthly income"
    ),
    Tool(
        name="CardFilterAdvanced",
        func=lambda profile_json: filter_cards_advanced(eval(profile_json)),
        description="Filter cards based on income, reward type, and preferred perks."
    ),
    Tool(
        name="RewardSimulator",
        func=lambda q: simulate_reward(q),
        description="Simulates cashback rewards based on monthly income"
    )
]

# Initialize agent
memory = ConversationBufferMemory(memory_key="chat_history")
agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent="chat-zero-shot-react-description",
    memory=memory,
    verbose=False
)

# Streamlit setup
st.set_page_config(page_title="💬 Chat Advisor", layout="centered")
st.title("💬 Credit Card Chat Advisor")

# Init session history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display past messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Chat input
user_prompt = st.chat_input("Ask me anything about credit cards...")

if user_prompt:
    # Show user message
    st.chat_message("user").markdown(user_prompt)
    st.session_state.messages.append({"role": "user", "content": user_prompt})

    try:
        # Get response from agent
        response = agent.invoke(user_prompt)
    except Exception as e:
        response = f"⚠️ Error: {str(e)}"

    # Show bot message
    st.chat_message("assistant").markdown(response)
    st.session_state.messages.append({"role": "assistant", "content": response})
