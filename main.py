from dotenv import load_dotenv
import os
from langchain_community.chat_models import ChatOpenAI
from langchain.agents import initialize_agent, Tool
from langchain.memory import ConversationBufferMemory
from langchain.agents import AgentType

from tools import filter_cards_by_income, simulate_reward, filter_cards_advanced

# ✅ Load environment variables
load_dotenv()
api_key = os.getenv("OPENROUTER_API_KEY")

# starting the LLM
llm = ChatOpenAI(
    openai_api_key=api_key,
    base_url="https://openrouter.ai/api/v1",
     model="anthropic/claude-3-haiku"  # model used is calude open-ai have paid API tokens
)


# working of tools
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

# memory for the LLM so that it can store the previous ans
memory = ConversationBufferMemory(memory_key="chat_history")

# Agent for the LangChain
agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    memory=memory,
    verbose=True,
    handle_parsing_errors=True,
    agent_kwargs={
        "system_message": (
            "You are a helpful credit card advisor. Always use the tools provided to answer the user's query. "
            "If the user mentions income, reward type, or perks (like lounge access), call the most relevant tool."
        )
    }
)




# Interactive loop
if __name__ == "__main__":
    print(" Credit Card Advisor is ready! Type 'exit' to quit.\n")
    while True:
        user_input = input("You: ")
        if user_input.lower() in ["exit", "quit"]:
            print(" Goodbye!")
            break
        try:
            response = agent.run(user_input)
            print("Bot:", response, "\n")
        except Exception as e:
            print(" Error:", str(e))
