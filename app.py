import streamlit as st

movie_rows = [
    {
        "title": "Trending Now",
        "shows": ["Stranger Things", "You", "Wednesday", "Lupin", "Arcane", "The Witcher"],
    },
    {
        "title": "Top Picks for You",
        "shows": ["Peaky Blinders", "Money Heist", "Dark", "Ozark", "Black Mirror", "Narcos"],
    },
    {
        "title": "Continue Watching",
        "shows": ["The Crown", "Breaking Bad", "The Night Agent", "The Sandman", "Bodies", "Cobra Kai"],
    },
]

show_colors = ["#e50914", "#4c1d95", "#0ea5e9", "#f59e0b", "#10b981", "#ec4899"]


def total_show_count(rows: list[dict]) -> int:
    return sum(len(row["shows"]) for row in rows)


st.set_page_config(page_title="Netflix Clone - Streamlit", layout="wide")

st.markdown(
    """
    <style>
      .stApp { background: #141414; color: #f5f5f5; }
      .navbar {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 1.25rem;
      }
      .logo { color: #e50914; font-size: 2rem; font-weight: 700; letter-spacing: 1px; }
      .meta { color: #9ca3af; font-size: 0.8rem; text-transform: uppercase; letter-spacing: 0.08em; }
      .hero {
        background: radial-gradient(circle at 20% 10%, #1f2937, #111 55%);
        border-radius: 14px;
        padding: 3rem 2rem;
        margin-bottom: 1.5rem;
      }
      .badge {
        display: inline-block;
        background: #e50914;
        border-radius: 999px;
        padding: 0.2rem 0.6rem;
        font-size: 0.8rem;
        margin-bottom: 0.8rem;
      }
      .hero-title { font-size: clamp(2rem, 3vw, 3rem); font-weight: 700; margin: 0.2rem 0 0.8rem; }
      .hero-text { color: #d1d5db; max-width: 620px; margin-bottom: 1rem; }
      .section-title { font-size: 1.2rem; margin: 1rem 0 0.7rem; font-weight: 600; }
      .card {
        border-radius: 10px;
        padding: 0.8rem;
        min-height: 150px;
        display: flex;
        align-items: flex-end;
        font-weight: 600;
      }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    f"""
    <div class=\"navbar\">
      <div>
        <div class=\"logo\">NETFLIX</div>
        <div class=\"meta\">{total_show_count(movie_rows)} Titles</div>
      </div>
      <div class=\"meta\">Home · TV Shows · Movies · My List</div>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <section class="hero">
      <div class="badge">New Series</div>
      <h2 class="hero-title">Galactic Frontier</h2>
      <p class="hero-text">A reluctant pilot joins a rebel crew to expose a hidden empire conspiracy across the stars.</p>
    </section>
    """,
    unsafe_allow_html=True,
)

for row in movie_rows:
    st.markdown(f"<h3 class='section-title'>{row['title']}</h3>", unsafe_allow_html=True)
    columns = st.columns(len(row["shows"]))
    for idx, (col, show) in enumerate(zip(columns, row["shows"], strict=False)):
        color = show_colors[idx % len(show_colors)]
        with col:
            st.markdown(
                (
                    "<div class='card' style=\""
                    f"background: linear-gradient(140deg, {color}, #111827);"
                    "\">"
                    f"{show}"
                    "</div>"
                ),
                unsafe_allow_html=True,
            )
