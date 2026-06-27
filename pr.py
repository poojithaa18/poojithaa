import streamlit as st
import random

# -----------------------------
# Page Config
# -----------------------------
st.set_page_config(page_title="Number Guessing Game", page_icon="🎯", layout="centered")

# -----------------------------
# Helper Functions
# -----------------------------
def hearts(rem, total):
    return "❤️ " * rem + "🤍 " * (total - rem)

def bar(rem, total):
    pct = rem / total if total else 0
    filled = int(pct * 20)
    return "█" * filled + "░" * (20 - filled)

def closeness(diff):
    if diff==0: return "🎉 Correct!"
    if diff<=3: return "🔥 Extremely Hot too close-chaalaa dagarlo unav"
    if diff<=7: return "🔥 Very Hot nearby around less 7 numbers"
    if diff<=15: return "🌡 Warm nearby around less 15 numbers"
    if diff<=30: return "❄️ Cold nearby around less 30 numbers"
    return "🥶 assalu number daridhapulo ledhu"
# -----------------------------
# Initialize Session State
# -----------------------------
defaults = {
    "secret": None,
    "remaining": 0,
    "total": 0,
    "score": 0,
    "history": [],
    "game_over": True,
    "message": "Set your range and chances, then start the game.",
    "tone": "info",
}
for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value

# -----------------------------
# Minimal styling
# -----------------------------
st.markdown(
    """
    <style>
    .stApp { max-width: 640px; margin: 0 auto; }
    div[data-testid="stForm"] {
        border: 1px solid rgba(128,128,128,0.25);
        border-radius: 12px;
        padding: 1.25rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# -----------------------------
# Title
# -----------------------------
st.title("🎯 Poojithaa Number Guessing Game")
st.caption("Guess the secret number with as few tries as possible.")

# -----------------------------
# Setup (only shown before a game starts, or after Play Again)
# -----------------------------
if st.session_state.secret is None:
    with st.container(border=True):
        st.subheader("Game setup")
        col1, col2, col3 = st.columns(3)
        with col1:
            min_num = st.number_input("Minimum", value=1, step=1, key="min_num")
        with col2:
            max_num = st.number_input("Maximum", value=100, step=1, key="max_num")
        with col3:
            chances = st.selectbox("Chances", [5, 6, 7, 8, 9, 10], index=2, key="chances")

        if st.button("▶️ Start game", type="primary", use_container_width=True):
            if min_num >= max_num:
                st.error("Minimum must be less than maximum.")
            else:
                st.session_state.secret = random.randint(int(min_num), int(max_num))
                st.session_state.remaining = chances
                st.session_state.total = chances
                st.session_state.score = 0
                st.session_state.history = []
                st.session_state.game_over = False
                st.session_state.message = f"Guess a number between {int(min_num)} and {int(max_num)}."
                st.session_state.tone = "info"
                st.session_state.min_for_round = int(min_num)
                st.session_state.max_for_round = int(max_num)
                st.rerun()

# -----------------------------
# Active game / result screen
# -----------------------------
else:
    # Status row
    st.markdown(f"### {hearts(st.session_state.remaining, st.session_state.total)}")
    st.code(bar(st.session_state.remaining, st.session_state.total), language=None)
    st.markdown(f"🏆 **Score:** {st.session_state.score}")

    # Message box
    tone = st.session_state.tone
    if tone == "success":
        st.success(st.session_state.message)
    elif tone == "error":
        st.error(st.session_state.message)
    else:
        st.info(st.session_state.message)

    # -----------------------------
    # Guess form — Enter key submits because it's inside st.form
    # -----------------------------
    if not st.session_state.game_over:
        with st.form(key="guess_form", clear_on_submit=True):
            guess = st.number_input("Your guess", step=1, value=None, key="guess_input")
            submitted = st.form_submit_button("🎲 Guess", type="primary", use_container_width=True)

        if submitted:
            if guess is None:
                st.warning("Enter a number before guessing.")
            else:
                guess = int(guess)
                st.session_state.remaining -= 1
                diff = abs(guess - st.session_state.secret)
                hint = closeness(diff)

                st.session_state.history.append((guess, hint))

                if guess == st.session_state.secret:
                    st.session_state.game_over = True
                    st.session_state.score = st.session_state.remaining * 20 + 20
                    st.session_state.message = (
                        f"🎉 You won! Correct number: {st.session_state.secret}. "
                        f"Score: {st.session_state.score}"
                    )
                    st.session_state.tone = "success"
                elif st.session_state.remaining <= 0:
                    st.session_state.game_over = True
                    st.session_state.message = f"💥 Game over. Correct number: {st.session_state.secret}"
                    st.session_state.tone = "error"
                elif guess < st.session_state.secret:
                    st.session_state.message = f"📉 Too low. {hint}"
                    st.session_state.tone = "info"
                else:
                    st.session_state.message = f"📈 Too high. {hint}"
                    st.session_state.tone = "info"

                st.rerun()

    # -----------------------------
    # Play again
    # -----------------------------
    if st.session_state.game_over:
        if st.button("🔄 Play again", use_container_width=True):
            for key in ["secret", "remaining", "total", "score", "history"]:
                st.session_state[key] = defaults[key]
            st.session_state.game_over = True
            st.session_state.message = "Set your range and chances, then start the game."
            st.session_state.tone = "info"
            st.rerun()

    # -----------------------------
    # History
    # -----------------------------
    st.subheader("📜 Guess history")
    if st.session_state.history:
        for g, h in reversed(st.session_state.history):
            st.write(f"**{g}** ➜ {h}")
    else:
        st.write("No guesses yet.")