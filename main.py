# main.py
import streamlit as st
from art import display_logo, display_card_image
from work import deal_card, calculate_score, compare

st.sidebar.markdown("### Game Rules:")
st.sidebar.text("Welcome to the Blackjack Game! Here's how to play:")

st.sidebar.markdown("1. **Objective:**")
st.sidebar.text("Your goal is to get as close to 21 points as possible without going over. If your total exceeds 21, you lose.")

st.sidebar.markdown("2. **Card Values:**")
st.sidebar.text("   - Number cards are worth their face value.")
st.sidebar.text("   - Face cards (Jack, Queen, King) are each worth 10 points.")
st.sidebar.text("   - Aces can be counted as 1 or 11, depending on your total.")

st.sidebar.markdown("3. **Game Flow:**")
st.sidebar.text("   - Click 'Start Game' to begin a new round.")
st.sidebar.text("   - You will be dealt two cards initially. You can then choose to draw additional cards ('+ Card').")
st.sidebar.text("   - Decide when to stop drawing cards and click 'Confirm Decision'. The computer will then draw its cards.")
st.sidebar.text("   - After the computer's turn, the winner will be determined based on the total points.")

st.sidebar.markdown("4. **Winning:**")
st.sidebar.text("   - If your total is closer to 21 than the computer's total, you win!")
st.sidebar.text("   - If the computer's total is closer to 21 or if you exceed 21, you lose.")

st.sidebar.markdown("5. **Play Again:**")
st.sidebar.text("   - After each round, you can click 'Play Again' to start a new game.")

st.sidebar.text("Enjoy the game and good luck!")


# Initialize session state
if 'user_cards' not in st.session_state:
    st.session_state.user_cards = []
if 'computer_cards' not in st.session_state:
    st.session_state.computer_cards = []
if 'user_score' not in st.session_state:
    st.session_state.user_score = 0
if 'computer_score' not in st.session_state:
    st.session_state.computer_score = 0
if 'game_in_progress' not in st.session_state:
    st.session_state.game_in_progress = False
if 'show_final_result' not in st.session_state:
    st.session_state.show_final_result = False

st.title("♥️♦️Blackjack Game♣️♠️")

display_logo()

if not st.session_state.show_final_result:
    if not st.session_state.game_in_progress and st.button("Start Game"):
        st.sidebar.markdown("### Game Rules:")
        st.sidebar.text("Your goal is to get as close to 21 as possible without going over.")
        st.sidebar.text("If your total exceeds 21, you lose.")
        st.sidebar.text("Face cards (Jack, Queen, King) are each worth 10.")
        st.sidebar.text("Aces can be counted as 1 or 11, depending on your total.")

        # Reset session state for a new game
        st.session_state.user_cards = []
        st.session_state.computer_cards = []
        st.session_state.user_score = 0
        st.session_state.computer_score = 0

        # Draw initial two cards
        for _ in range(2):
            st.session_state.user_cards.append(deal_card())
            st.session_state.computer_cards.append(deal_card())

        st.session_state.user_score = calculate_score(st.session_state.user_cards)
        st.session_state.computer_score = calculate_score(st.session_state.computer_cards)

        col1,col2 = st.columns(2)
        with col1:
            st.write(f"Your initial hand: {st.session_state.user_cards}, current score: {st.session_state.user_score}")
            for i in st.session_state.user_cards:
                display_card_image(i)
        
        with col2:
            st.write(f"Computer's first card: {st.session_state.computer_cards[0]}")
            display_card_image(st.session_state.computer_cards[0])

        st.session_state.game_in_progress = True

    if st.session_state.game_in_progress:
        if st.button("+ Card"):
            drawn_card = deal_card()
            st.session_state.user_cards.append(drawn_card)
            st.session_state.user_score = calculate_score(st.session_state.user_cards)
            user_score_with_ace_as_1 = calculate_score(st.session_state.user_cards, ace_as_1=True)
            user_score_with_ace_as_11 = calculate_score(st.session_state.user_cards, ace_as_1=False)
            st.write(f"Your hand: {st.session_state.user_cards}, current score: {user_score_with_ace_as_1} or {user_score_with_ace_as_11}")

            for i in st.session_state.user_cards:
                display_card_image(i)

        if st.button("Confirm Decision"):
            while st.session_state.computer_score < 17:
                st.session_state.computer_cards.append(deal_card())
                st.session_state.computer_score = calculate_score(st.session_state.computer_cards)

            col1,col2 = st.columns(2)
            with col1:
                st.write(f"Your final hand: {st.session_state.user_cards}, final score: {st.session_state.user_score}")
                for i in st.session_state.user_cards:
                    display_card_image(i)
            with col2:
                st.write(f"Computer's final hand: {st.session_state.computer_cards}, final score: {st.session_state.computer_score}")
                for i in st.session_state.computer_cards:
                    display_card_image(i)
            result = compare(st.session_state.user_score, st.session_state.computer_score)
            st.write(result)

            # Set the flag to show final result
            st.session_state.show_final_result = True

if st.session_state.show_final_result:
    # Show the "Play Again" button after confirming the decision
    if st.button("Play Again"):
        # Reset session state for a new game
        st.session_state.user_cards = []
        st.session_state.computer_cards = []
        st.session_state.user_score = 0
        st.session_state.computer_score = 0
        st.session_state.game_in_progress = False
        st.session_state.show_final_result = False
