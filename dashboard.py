import streamlit as st
import pandas as pd
import plotly.express as px

from app.analytics import load_games
from app.services.game_service import update_game_catalogue
from app.integrations.rawg import search_games
from app.integrations.gamerpower import get_free_games
from app.integrations.cheapshark import get_game_deals

BG = "rgba(0,0,0,0)"

st.set_page_config(
    page_title="GameScope",
    page_icon="\U0001F3AE",
    layout="wide",
)

if "search_query" not in st.session_state:
    st.session_state.search_query = ""


def set_search(title: str):
    st.session_state.search_query = title


@st.cache_data(ttl=3600, show_spinner=False)
def get_cover_image(title: str):
    try:
        matches = search_games(title, page_size=1)
        if matches and matches[0].get("background_image"):
            return matches[0]["background_image"]
    except Exception:
        pass
    return None


@st.cache_data(ttl=600, show_spinner=False)
def fetch_cached_free_games():
    return get_free_games()


@st.cache_data(ttl=600, show_spinner=False)
def fetch_cached_deals(limit: int = 10):
    return get_game_deals(limit=limit)


def render_rec_card(rec: dict, idx: int):
    with st.container(border=True):
        img_url = rec.get("background_image") or get_cover_image(rec["name"])
        if img_url:
            st.image(img_url, use_container_width=True)
        st.markdown(f"**{rec['name']}**")
        meta = rec.get("metacritic")
        meta_txt = f" | Metacritic: {int(meta)}" if pd.notna(meta) else ""
        st.caption(f"Rating: {rec.get('rating', 'N/A')} / 5{meta_txt}")
        st.button(
            "Inspect Title",
            key=f"rec_btn_{idx}",
            on_click=set_search,
            args=(rec["name"],),
            use_container_width=True,
        )


def render_game_card(game: dict):
    with st.container(border=True):
        img_c, info_c = st.columns([1.2, 2])
        if game.get("background_image"):
            img_c.image(game["background_image"], use_container_width=True)
        info_c.markdown(f"### {game['name']}")
        released = game.get("released") or "TBA"
        rating = game.get("rating") or "N/A"
        meta = game.get("metacritic") or "N/A"
        info_c.markdown(
            f"<span class='meta-badge'>Rating: {rating} / 5</span>"
            f"<span class='meta-badge'>Metacritic: {meta}</span>"
            f"<span class='meta-badge'>Released: {released}</span>",
            unsafe_allow_html=True,
        )
        genres = ", ".join([g["name"] for g in game.get("genres", [])[:3]])
        if genres:
            info_c.caption(f"Genres: {genres}")


def render_free_card(fg: dict):
    with st.container(border=True):
        c_img, c_info = st.columns([1.2, 2.3])
        if fg.get("thumbnail"):
            c_img.image(fg["thumbnail"], use_container_width=True)
        c_info.markdown(f"#### {fg['title']}")
        worth = fg.get("worth", "Free")
        platforms = fg.get("platforms", "PC")
        g_type = fg.get("type", "Game")
        c_info.markdown(
            f"<span class='deal-badge'>FREE (Worth {worth})</span>"
            f"<span class='meta-badge'>{platforms}</span>"
            f"<span class='meta-badge'>{g_type}</span>",
            unsafe_allow_html=True,
        )
        if fg.get("open_giveaway_url"):
            c_info.link_button("Claim Giveaway", fg["open_giveaway_url"], use_container_width=True)


def render_deal_card(deal: dict):
    with st.container(border=True):
        c_img, c_info = st.columns([1, 2.5])
        if deal.get("thumb"):
            c_img.image(deal["thumb"], use_container_width=True)
        c_info.markdown(f"#### {deal['title']}")
        sale = float(deal.get("salePrice", 0))
        normal = float(deal.get("normalPrice", 0))
        savings = int(round(float(deal.get("savings", 0))))
        rating = deal.get("dealRating", "N/A")
        c_info.markdown(
            f"<span class='deal-badge'>-{savings}% OFF</span>"
            f"<span class='meta-badge'>Now ${sale:.2f} (Was ${normal:.2f})</span>"
            f"<span class='meta-badge'>Deal Score: {rating}/10</span>",
            unsafe_allow_html=True,
        )
        deal_id = deal.get("dealID")
        if deal_id:
            url = f"https://www.cheapshark.com/redirect?dealID={deal_id}"
            c_info.link_button("View Store Deal", url, use_container_width=True)


st.markdown(
    """
    <style>
    [data-testid="stMetric"] {
        background: #141824;
        border: 1px solid #2d3548;
        border-left: 4px solid #7c4dff;
        padding: 14px 18px;
        border-radius: 10px;
    }
    .hero-banner {
        background: linear-gradient(90deg, #1e1b4b, #311042, #111827);
        padding: 20px 26px;
        border-radius: 12px;
        border: 1px solid #3730a3;
        margin-bottom: 18px;
    }
    .hero-banner h1 { margin: 0; color: #f8fafc; font-size: 2rem; }
    .hero-banner p { margin: 6px 0 0 0; color: #cbd5e1; }
    .meta-badge {
        display: inline-block;
        background: #1e293b;
        border: 1px solid #475569;
        color: #e2e8f0;
        padding: 3px 10px;
        border-radius: 999px;
        font-size: 0.82rem;
        margin-right: 6px;
        margin-bottom: 6px;
    }
    .deal-badge {
        display: inline-block;
        background: #14532d;
        border: 1px solid #22c55e;
        color: #bbf7d0;
        font-weight: 700;
        padding: 3px 10px;
        border-radius: 999px;
        font-size: 0.82rem;
        margin-right: 6px;
        margin-bottom: 6px;
    }
    </style>
    <div class="hero-banner">
        <h1>&#127918; GameScope &mdash; Video Game Discovery &amp; Analytics</h1>
        <p>Market telemetry, critic vs. player ratings, free giveaways, and PC deals.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

with st.sidebar:
    st.header("Control Panel")
    if st.button("Sync Latest Games", use_container_width=True, type="primary"):
        with st.spinner("Syncing from RAWG..."):
            res = update_game_catalogue()
        st.success(f"Synced {res['processed']} games!")
        st.rerun()

    st.divider()
    hide_unrated = st.toggle("Hide unrated / TBA (rating = 0)", value=True)
    top_n = st.slider("Top Games Count", 5, 20, 10)

tab1, tab2, tab3 = st.tabs(["Analytics", "Game Explorer", "Free Games & Deals"])

# --- TAB 1: ANALYTICS ---
with tab1:
    df = load_games()
    if df.empty:
        st.warning("No games in database yet. Click Sync Latest Games.")
    else:
        fdf = df[df["rating"] > 0].copy() if hide_unrated else df.copy()

        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Stored Games", len(fdf))
        avg_r = f"{fdf['rating'].mean():.2f} / 5" if not fdf.empty else "N/A"
        c2.metric("Avg Player Rating", avg_r)
        max_r = f"{fdf['rating'].max():.2f}" if not fdf.empty else "N/A"
        c3.metric("Highest Rating", max_r)
        avg_m = fdf["metacritic"].dropna().mean()
        c4.metric("Avg Metacritic", f"{avg_m:.0f} / 100" if pd.notna(avg_m) else "N/A")

        col_l, col_r = st.columns([1.3, 1])

        with col_l:
            top = fdf.dropna(subset=["rating"]).nlargest(top_n, "rating")
            fig_bar = px.bar(
                top,
                x="rating",
                y="name",
                orientation="h",
                color="rating",
                color_continuous_scale="Purp",
                text="rating",
                title=f"Top {len(top)} Highest-Rated Games",
            )
            fig_bar.update_traces(texttemplate="%{text:.2f}", textposition="outside")
            fig_bar.update_layout(
                template="plotly_dark",
                paper_bgcolor=BG,
                plot_bgcolor=BG,
                yaxis={"categoryorder": "total ascending"},
                coloraxis_showscale=False,
                xaxis_range=[0, 5.4],
                height=420,
            )
            st.plotly_chart(fig_bar, use_container_width=True)

        with col_r:
            fig_hist = px.histogram(
                fdf.dropna(subset=["rating"]),
                x="rating",
                nbins=15,
                color_discrete_sequence=["#7c4dff"],
                title="Rating Distribution",
            )
            fig_hist.update_layout(
                template="plotly_dark",
                paper_bgcolor=BG,
                plot_bgcolor=BG,
                bargap=0.12,
                height=420,
            )
            st.plotly_chart(fig_hist, use_container_width=True)

        meta_df = fdf.dropna(subset=["metacritic", "rating"])
        if not meta_df.empty:
            fig_scatter = px.scatter(
                meta_df,
                x="metacritic",
                y="rating",
                size="metacritic",
                color="rating",
                hover_name="name",
                color_continuous_scale="Turbo",
                title="Critic Score (Metacritic) vs. Player Rating (RAWG)",
            )
            fig_scatter.update_layout(
                template="plotly_dark",
                paper_bgcolor=BG,
                plot_bgcolor=BG,
                height=360,
            )
            st.plotly_chart(fig_scatter, use_container_width=True)

        cols = [c for c in ["name", "released", "rating", "metacritic", "source"] if c in fdf.columns]
        st.dataframe(
            fdf[cols].sort_values(by="rating", ascending=False),
            use_container_width=True,
            hide_index=True,
        )

# --- TAB 2: GAME EXPLORER ---
with tab2:
    st.subheader("Explore & Discover Games")
    s_col, b_col = st.columns([5, 1])
    with s_col:
        query = st.text_input(
            "Search RAWG database",
            key="search_query",
            label_visibility="collapsed",
            placeholder="Search any title (e.g., Elden Ring, Hades II, Cyberpunk 2077)...",
        )
    with b_col:
        st.button("Clear", on_click=set_search, args=("",), use_container_width=True)

    st.markdown("#### Top Recommended Titles")
    rec_df = load_games()
    if not rec_df.empty and (rec_df["rating"] > 0).any():
        top_recs = rec_df[rec_df["rating"] > 0].nlargest(4, "rating").to_dict("records")
    else:
        top_recs = [
            {"name": "The Witcher 3: Wild Hunt", "rating": 4.66, "metacritic": 92},
            {"name": "Elden Ring", "rating": 4.41, "metacritic": 96},
            {"name": "Disco Elysium: Final Cut", "rating": 4.67, "metacritic": 97},
            {"name": "Persona 5 Royal", "rating": 4.76, "metacritic": 95},
        ]

    rec_cols = st.columns(4)
    for idx, rec in enumerate(top_recs):
        with rec_cols[idx]:
            render_rec_card(rec, idx)

    st.divider()

    if query:
        with st.spinner(f"Searching RAWG for '{query}'..."):
            results = search_games(query, page_size=8)

        if not results:
            st.info(f"No games found matching '{query}'.")
        else:
            st.markdown(f"#### Search Results for *{query}* ({len(results)} found)")
            row_cols = st.columns(2)
            for idx, game in enumerate(results):
                with row_cols[idx % 2]:
                    render_game_card(game)

# --- TAB 3: FREE GAMES & DEALS ---
with tab3:
    h_col, r_col = st.columns([5, 1])
    with h_col:
        st.subheader("Live Giveaways & PC Store Discounts")
    with r_col:
        if st.button("Refresh Offers", use_container_width=True):
            fetch_cached_free_games.clear()
            fetch_cached_deals.clear()
            st.rerun()

    free_games = fetch_cached_free_games()
    deals = fetch_cached_deals(limit=10)

    m1, m2, m3 = st.columns(3)
    m1.metric("Active Giveaways", len(free_games))
    m2.metric("Featured PC Deals", len(deals))
    max_disc = max([int(round(float(d.get("savings", 0)))) for d in deals], default=0)
    m3.metric("Top Store Discount", f"{max_disc}% OFF")

    st.divider()

    col_free, col_deals = st.columns(2)
    with col_free:
        st.markdown("#### Free Giveaways (GamerPower)")
        for fg in free_games[:8]:
            render_free_card(fg)

    with col_deals:
        st.markdown("#### Top PC Deals (CheapShark)")
        for deal in deals[:8]:
            render_deal_card(deal)
