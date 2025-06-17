import streamlit as st
from tools import filter_cards_by_income, simulate_reward

st.set_page_config(page_title="Credit Card Advisor", layout="centered")

st.title("💳 AI-Powered Credit Card Advisor")
st.write("Get personalized credit card recommendations in seconds.")

# --- Form Input ---
with st.form("user_form"):
    income = st.number_input("What is your monthly income? (₹)", step=1000, min_value=1000)
    simulate = st.checkbox("Simulate rewards?")
    submit = st.form_submit_button("Get Recommendations")

# --- Output Section ---
if submit:
    st.subheader("🔎 Matching Credit Cards")
    raw_cards = filter_cards_by_income(income)

    if isinstance(raw_cards, str):  # If it's just a message
        st.warning(raw_cards)
    else:
        selected_cards = []
        for i, card in enumerate(raw_cards):
            with st.expander(f"{card['card_name']} ({card['issuer']})"):
                st.markdown(f"💰 **Joining Fee**: ₹{card['joining_fee']}")
                st.markdown(f"🏷️ **Reward Type**: {card['reward_type']}")
                st.markdown(f"🎯 **Reward Rate**: {card['reward_rate']}")
                st.markdown(f"✨ **Perks**: {', '.join(card['perks'])}")
                st.markdown(f"[🔗 Apply Here]({card['apply_link']})")
                if st.checkbox("Compare this card", key=f"compare_{i}"):
                    selected_cards.append(card)

        if selected_cards:
            st.subheader("📊 Compare Selected Cards")

            cols = st.columns(len(selected_cards))
            for idx, card in enumerate(selected_cards):
                with cols[idx]:
                    st.markdown(f"**{card['card_name']}**")
                    st.markdown(f"🏦 {card['issuer']}")
                    st.markdown(f"💸 ₹{card['joining_fee']}")
                    st.markdown(f"🎯 {card['reward_rate']}")
                    st.markdown(f"✨ {' | '.join(card['perks'])}")
                    st.markdown(f"[Apply]({card['apply_link']})")

    # Simulate reward
    if simulate:
        st.subheader("💰 Estimated Annual Rewards")
        reward = simulate_reward(income)
        st.success(reward)

    if st.button("🔁 Restart"):
        st.experimental_rerun()

