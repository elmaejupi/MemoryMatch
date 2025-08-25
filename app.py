# streamlit run app.py
import streamlit as st
import random
import time

st.set_page_config(page_title="🧠 Memory Match", page_icon="🧩", layout="centered")

# -----------------------
# Game Config & Helpers
# -----------------------
EMOJIS = [
    "🍎","🍌","🍇","🍒","🍉","🍍","🥝","🍑",
    "🍔","🍕","🌮","🍟","🍩","🍪","🍰","🧁",
    "⚽","🏀","🏈","🎾","🏐","🎱","🏓","🥇",
    "🚗","🚲","🛸","🛵","🚀","✈","🚂","🛳",
    "🐶","🐱","🐼","🦊","🐵","🐸","🦄","🐨",
    "🌙","⭐","☀","🌈","❄","⚡","🔥","💧",
]

GRID_PRESETS = {
    "Easy (4 x 4)": (4, 4),
    "Medium (4 x 6)": (4, 6),
    "Hard (6 x 6)": (6, 6),
}

def new_deck(rows: int, cols: int, seed: int | None = None):
    """Create a shuffled deck with pairs of symbols for the grid size."""
    assert (rows * cols) % 2 == 0, "Grid must have an even number of cells."
    pairs = (rows * cols) // 2
    rnd = random.Random(seed)
    picks = rnd.sample(EMOJIS, pairs)  # unique pairs
    deck = picks * 2
    rnd.shuffle(deck)
    return deck

def all_matched(matched_idx: set, total_cards: int) -> bool:
    return len(matched_idx) == total_cards

def reset_game(rows: int, cols: int, seed: int | None = None):
    st.session_state.rows = rows
    st.session_state.cols = cols
    st.session_state.total = rows * cols
    st.session_state.deck = new_deck(rows, cols, seed)
    st.session_state.matched = set()
    st.session_state.flipped = []             # indices currently face-up but not yet confirmed
    st.session_state.pending_mismatch = False # when two flipped are not a match; wait for user to continue
    st.session_state.moves = 0
    st.session_state.seed = seed if seed is not None else random.randint(1, 10_000_000)
    st.session_state.start_time = time.time()
    st.session_state.end_time = None
    st.session_state.game_over = False

def ensure_state_initialized():
    if "deck" not in st.session_state:
        r, c = GRID_PRESETS["Easy (4 x 4)"]
        reset_game(r, c)

def elapsed_seconds():
    if st.session_state.end_time:
        return int(st.session_state.end_time - st.session_state.start_time)
    return int(time.time() - st.session_state.start_time)

# -----------------------
# UI: Sidebar Controls
# -----------------------
st.title("🧠 Memory Match (Flip & Find Pairs)")
st.caption("Find all pairs with as few moves as possible!")

with st.sidebar:
    st.header("🎛 Game Settings")
    size_label = st.selectbox("Grid size", list(GRID_PRESETS.keys()))
    rows, cols = GRID_PRESETS[size_label]
    # Seed helps reproducible shuffles; leave blank for random each time
    user_seed = st.text_input("Shuffle seed (optional)", value="")
    seed_val = int(user_seed) if user_seed.strip().isdigit() else None

    if st.button("🆕 New Game"):
        reset_game(rows, cols, seed=seed_val)

# -----------------------
# Main Game Area
# -----------------------
ensure_state_initialized()

# If user changed preset via sidebar and hasn't pressed New Game yet, offer quick apply.
curr_rows, curr_cols = st.session_state.get("rows", rows), st.session_state.get("cols", cols)
if (rows, cols) != (curr_rows, curr_cols):
    st.info("Press *New Game* in the sidebar to apply the new grid size.")

# Header stats
cols_top = st.columns(3)
cols_top[0].metric("Moves", st.session_state.moves)
cols_top[1].metric("Matched", f"{len(st.session_state.matched)}/{st.session_state.total}")
cols_top[2].metric("Time (s)", elapsed_seconds())

st.divider()

# Helper to render a single card
def render_card(i: int):
    deck = st.session_state.deck
    flipped = st.session_state.flipped
    matched = st.session_state.matched
    pending_mismatch = st.session_state.pending_mismatch

    is_matched = i in matched
    is_flipped = (i in flipped)
    face = deck[i]

    disabled = is_matched or is_flipped or pending_mismatch or st.session_state.game_over
    label = face if (is_matched or is_flipped) else "❓"

    if st.button(label, key=f"card_{i}", use_container_width=True, disabled=disabled):
        on_card_click(i)

# Card click logic
def on_card_click(i: int):
    if st.session_state.game_over:
        return
    if i in st.session_state.matched or i in st.session_state.flipped:
        return

    st.session_state.flipped.append(i)

    # If two cards are flipped, evaluate
    if len(st.session_state.flipped) == 2:
        a, b = st.session_state.flipped
        st.session_state.moves += 1
        if st.session_state.deck[a] == st.session_state.deck[b]:
            # Match!
            st.session_state.matched.update([a, b])
            st.session_state.flipped = []
            if all_matched(st.session_state.matched, st.session_state.total):
                st.session_state.game_over = True
                st.session_state.end_time = time.time()
        else:
            # Not a match: freeze board until user acknowledges
            st.session_state.pending_mismatch = True

# Grid
container = st.container()
for r in range(st.session_state.rows):
    cols_row = container.columns(st.session_state.cols, gap="small")
    for c in range(st.session_state.cols):
        idx = r * st.session_state.cols + c
        with cols_row[c]:
            render_card(idx)

# Pending mismatch UI
if st.session_state.pending_mismatch:
    st.warning("❌ Not a match. Click *Continue* to turn the cards back over.")
    if st.button("🔁 Continue"):
        st.session_state.flipped = []
        st.session_state.pending_mismatch = False

# Win banner
if st.session_state.game_over:
    st.success(f"🏁 Completed in {st.session_state.moves} moves and {elapsed_seconds()} seconds! 🎉")

st.divider()
with st.expander("ℹ How to play", expanded=False):
    st.markdown(
        """
- Click two cards to reveal them.  
- If they match, they stay face-up. If not, press *Continue* to turn them back over.  
- Clear the board with the fewest moves possible.  
- Change *Grid size* or *Shuffle seed* from the sidebar → *New Game*.
        """
    )