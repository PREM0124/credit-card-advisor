import json
import pandas as pd

#  tking the data from card_data.json
def load_card_data():
    with open("card_data.json") as f:
        data = json.load(f)
    return pd.DataFrame(data)

# Tool 1: Filter cards based on monthly income
def filter_cards_by_income(income):
    df = load_card_data()
    income = int(income)

    def eligible(row):
        try:
            threshold = int(row['eligibility'].split(">")[1].strip())
            return income > threshold
        except:
            return True  # fallback if format is wrong

    filtered = df[df.apply(eligible, axis=1)]
    
    if filtered.empty:
        return " No matching cards found for your income."

    result = ""
    for _, row in filtered.iterrows():
        result += f"💳 {row['card_name']} ({row['issuer']})\n"
        result += f"    ₹{row['joining_fee']} joining fee\n"
        result += f"    Rewards: {row['reward_rate']}\n"
        result += f"    Perks: {', '.join(row['perks'])}\n"
        result += f"    Apply: {row['apply_link']}\n\n"
    return result

# Tool 2: Filter cards based on profiles
def filter_cards_advanced(income: int, reward_type: str, perks: list):
    df = load_card_data()
    income = int(income)
    preferred_type = reward_type.lower()
    desired_perks = [p.lower() for p in perks]

    def eligible(row):
        try:
            income_ok = income > int(row['eligibility'].split(">")[1].strip())
            reward_match = preferred_type in row['reward_type'].lower()
            perks_match = all(dp in [p.lower() for p in row['perks']] for dp in desired_perks)
            return income_ok and reward_match and perks_match
        except:
            return False

    filtered = df[df.apply(eligible, axis=1)]

    if filtered.empty:
        return "❌ No matching cards found for your preferences."

    result = ""
    for _, row in filtered.iterrows():
        result += f"💳 {row['card_name']} ({row['issuer']})\n"
        result += f"   🏷️ ₹{row['joining_fee']} fee | 🎯 {row['reward_rate']}\n"
        result += f"   ✨ Perks: {', '.join(row['perks'])}\n"
        result += f"   🔗 [Apply Here]({row['apply_link']})\n\n"
    return result


#  Tool 3: Simulate reward based on income
def simulate_reward(income):
    try:
        income = int(income)
    except:
        return "❌ Please enter a valid number for income."

    reward_month = income * 0.05  # Assume 5% average reward
    reward_year = reward_month * 12
    return f"🧮 With ₹{income}/month income, you could earn approx ₹{int(reward_year)} per year in rewards (at 5%)."
