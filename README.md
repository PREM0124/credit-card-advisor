# Credit Card Advisor (AI-Powered)

This is a smart credit card recommendation tool I built using OpenAI, LangChain, and Streamlit. The idea was to make credit card selection simpler and more personalized by using conversational AI and filtering logic.

The user just needs to chat or answer a few simple questions like income, reward preferences, or desired perks, and the assistant recommends the best cards accordingly. You can also simulate estimated rewards and compare multiple cards side by side.

---

# Features

- Chat-based and form-style interface
- Filters cards by income, reward type (cashback/points), and perks (like lounge access)
- Simulates estimated yearly rewards
- Side-by-side comparison of selected cards
- Easy to restart or explore again
- Mobile-friendly UI

---

#Tech Stack

- **Python**
- **LangChain** (tools, memory, agent)
- **OpenAI GPT** (used via API)
- **Streamlit** (for frontend UI)
- **Pandas** (for handling card data)

---

# Dataset

I manually created a dataset of 15+ Indian credit cards including options from HDFC, SBI, Axis, and ICICI. Each entry includes:
- Card name and issuer
- Joining fee
- Reward type and rate
- Perks like cashback, lounge access, fuel waivers
- A dummy application link

You can easily extend this by scraping from trusted card review sites.

---

# How to Run Locally

```bash
git clone https://github.com/PREM0124/credit-card-advisor.git
cd credit-card-advisor

# Create virtual environment
python -m venv venv
venv\Scripts\activate   # or source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Add your OpenAI API key in .env
echo OPENAI_API_KEY=your-api-key > .env

# Run the app
streamlit run chat_app.py
