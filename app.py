import pickle
import streamlit as st
import requests
import pandas as pd

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(page_title="CineMatch", layout="wide", page_icon="🎬")

# ── CSS ───────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Barlow:wght@300;400;600&display=swap');

html, body, [class*="css"] {
    background-color: #141414 !important;
    color: #fff !important;
    font-family: 'Barlow', sans-serif;
}
#MainMenu, footer, header { visibility: hidden; }

.hero {
    background: linear-gradient(135deg, #e50914 0%, #b20710 40%, #141414 100%);
    padding: 3rem 2rem 2rem;
    border-radius: 0 0 40px 40px;
    margin-bottom: 2rem;
    position: relative;
    overflow: hidden;
}
.hero::before {
    content: '';
    position: absolute;
    top: -50%; right: -20%;
    width: 600px; height: 600px;
    background: rgba(255,255,255,0.03);
    border-radius: 50%;
}
.hero-logo {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 3.5rem;
    letter-spacing: 4px;
    color: #fff;
    text-shadow: 0 0 40px rgba(229,9,20,0.8);
    margin: 0;
}
.hero-tagline {
    font-size: 1rem;
    color: rgba(255,255,255,0.6);
    font-weight: 300;
    letter-spacing: 2px;
    margin-top: 0.2rem;
}

div[data-baseweb="select"] > div {
    background-color: #2a2a2a !important;
    border: 1px solid #444 !important;
    border-radius: 8px !important;
    color: white !important;
}

.stButton > button {
    background: #e50914 !important;
    color: white !important;
    font-family: 'Bebas Neue', sans-serif !important;
    font-size: 1.1rem !important;
    letter-spacing: 3px !important;
    border: none !important;
    border-radius: 6px !important;
    padding: 0.6rem 2.5rem !important;
    width: 100% !important;
    margin-top: 0.4rem !important;
    transition: all 0.2s ease !important;
}
.stButton > button:hover {
    background: #ff0a16 !important;
    transform: scale(1.02) !important;
    box-shadow: 0 6px 25px rgba(229,9,20,0.5) !important;
}

.section-title {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 1.6rem;
    letter-spacing: 3px;
    color: #fff;
    margin: 2rem 0 1rem;
    padding-left: 0.5rem;
    border-left: 4px solid #e50914;
}

/* ── Movie card ── */
.movie-card {
    position: relative;
    border-radius: 12px;
    overflow: hidden;
    background: #1a1a1a;
    margin-bottom: 1.5rem;
    transition: transform 0.3s ease, box-shadow 0.3s ease;
    border: 1px solid #2a2a2a;
}
.movie-card:hover {
    transform: translateY(-6px);
    box-shadow: 0 16px 45px rgba(229,9,20,0.35);
}
.movie-card img {
    width: 100%;
    display: block;
    min-height: 260px;
    object-fit: cover;
    border-radius: 12px 12px 0 0;
}
.movie-rank {
    position: absolute;
    top: 10px; left: 10px;
    background: #e50914;
    color: white;
    font-family: 'Bebas Neue', sans-serif;
    font-size: 1rem;
    padding: 2px 10px;
    border-radius: 4px;
    letter-spacing: 1px;
}
.movie-rating {
    position: absolute;
    top: 10px; right: 10px;
    background: rgba(0,0,0,0.75);
    color: #f5c518;
    font-size: 0.8rem;
    font-weight: 600;
    padding: 3px 8px;
    border-radius: 20px;
    letter-spacing: 0.5px;
}
.movie-info {
    padding: 0.9rem 1rem;
    background: #1a1a1a;
    border-radius: 0 0 12px 12px;
}
.movie-info-title {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 1.05rem;
    letter-spacing: 1px;
    color: #fff;
    margin-bottom: 0.3rem;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}
.movie-info-meta {
    display: flex;
    gap: 8px;
    flex-wrap: wrap;
    margin-bottom: 0.4rem;
}
.meta-tag {
    background: #2a2a2a;
    color: rgba(255,255,255,0.6);
    font-size: 0.7rem;
    padding: 2px 8px;
    border-radius: 20px;
    letter-spacing: 0.5px;
}
.meta-tag-genre {
    background: rgba(229,9,20,0.2);
    color: #ff6b6b;
    font-size: 0.7rem;
    padding: 2px 8px;
    border-radius: 20px;
    letter-spacing: 0.5px;
}
.movie-info-overview {
    font-size: 0.75rem;
    color: rgba(255,255,255,0.45);
    line-height: 1.5;
    display: -webkit-box;
    -webkit-line-clamp: 3;
    -webkit-box-orient: vertical;
    overflow: hidden;
    margin-top: 0.4rem;
}

.netflix-divider {
    border: none;
    height: 1px;
    background: linear-gradient(to right, #e50914, transparent);
    margin: 1.5rem 0;
}
.select-label {
    font-size: 0.8rem;
    letter-spacing: 2px;
    text-transform: uppercase;
    color: rgba(255,255,255,0.4);
    margin-bottom: 0.3rem;
}
.empty-state {
    text-align: center;
    padding: 4rem 0;
    color: rgba(255,255,255,0.15);
}
.empty-state-title {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 3.5rem;
    letter-spacing: 4px;
}
.empty-state-sub {
    font-size: 1rem;
    letter-spacing: 2px;
    margin-top: 0.5rem;
}
</style>
""", unsafe_allow_html=True)

# ── Load model ────────────────────────────────────────────────────────────────
@st.cache_resource
def load_model():
    movies_dict = pickle.load(open('movies_dic.pkl', 'rb'))
    similarity  = pickle.load(open('similar.pkl', 'rb'))
    movies = pd.DataFrame(movies_dict).reset_index(drop=True)
    return movies, similarity

movies, similarity = load_model()

# ── Fetch full movie details from TMDB ───────────────────────────────────────
@st.cache_data
def fetch_movie_details(movie_id):
    try:
        r = requests.get(
            f'https://api.themoviedb.org/3/movie/{movie_id}'
            f'?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US',
            timeout=5
        )
        data = r.json()
        poster = (
            'https://image.tmdb.org/t/p/w500' + data['poster_path']
            if data.get('poster_path') else
            'https://via.placeholder.com/500x750/1f1f1f/e50914?text=No+Poster'
        )
        genres = [g['name'] for g in data.get('genres', [])[:2]]
        year   = data.get('release_date', '')[:4] or 'N/A'
        rating = round(data.get('vote_average', 0), 1)
        runtime = data.get('runtime', 0)
        overview = data.get('overview', 'No overview available.')
        return {
            'poster':   poster,
            'genres':   genres,
            'year':     year,
            'rating':   rating,
            'runtime':  f"{runtime} min" if runtime else 'N/A',
            'overview': overview,
        }
    except Exception:
        return {
            'poster':   'https://via.placeholder.com/500x750/1f1f1f/e50914?text=No+Poster',
            'genres':   [],
            'year':     'N/A',
            'rating':   0,
            'runtime':  'N/A',
            'overview': 'No overview available.',
        }

# ── Recommend function (10 movies) ───────────────────────────────────────────
def recommend(movie, n=10):
    try:
        index = movies[movies['title'] == movie].index[0]
        distances = sorted(
            list(enumerate(similarity[index])),
            reverse=True, key=lambda x: x[1]
        )
        results = []
        for i in distances[1:n+1]:
            row     = movies.iloc[i[0]]
            details = fetch_movie_details(row['movie_id'])
            results.append({'title': row['title'], **details})
        return results
    except Exception as e:
        st.error(f"Something went wrong: {e}")
        return []

# ── Render a single movie card ────────────────────────────────────────────────
def render_card(rank, title, details):
    genres_html = "".join(
        f'<span class="meta-tag-genre">{g}</span>' for g in details['genres']
    )
    st.markdown(f"""
    <div class="movie-card">
        <img src="{details['poster']}" alt="{title}"/>
        <div class="movie-rank">#{rank}</div>
        <div class="movie-rating">⭐ {details['rating']}</div>
        <div class="movie-info">
            <div class="movie-info-title">{title}</div>
            <div class="movie-info-meta">
                <span class="meta-tag">📅 {details['year']}</span>
                <span class="meta-tag">⏱ {details['runtime']}</span>
                {genres_html}
            </div>
            <div class="movie-info-overview">{details['overview']}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ── Hero ──────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <p class="hero-logo">🎬 MOVIES STORE </p>
    <p class="hero-tagline">know your fav</p>
</div>
""", unsafe_allow_html=True)

# ── Search ────────────────────────────────────────────────────────────────────
col_sel, col_btn = st.columns([4, 1])
with col_sel:
    st.markdown('<p class="select-label">Choose a movie you love</p>', unsafe_allow_html=True)
    selected_movie = st.selectbox("", movies['title'].values, label_visibility="collapsed")
with col_btn:
    st.markdown("<br>", unsafe_allow_html=True)
    find = st.button("▶ FIND MATCHES")

st.markdown('<hr class="netflix-divider">', unsafe_allow_html=True)

# ── Results ───────────────────────────────────────────────────────────────────
if find:
    with st.spinner("🎬 Finding your perfect matches..."):
        results = recommend(selected_movie, n=10)

    if results:
        st.markdown(f'<p class="section-title">BECAUSE YOU WATCHED: {selected_movie.upper()}</p>',
                    unsafe_allow_html=True)

        # Row 1 — first 5
        st.markdown("##### Top Picks")
        cols1 = st.columns(5)
        for idx, col in enumerate(cols1):
            with col:
                render_card(idx + 1, results[idx]['title'], results[idx])

        st.markdown('<hr class="netflix-divider">', unsafe_allow_html=True)

        # Row 2 — next 5
        st.markdown("##### More Like This")
        cols2 = st.columns(5)
        for idx, col in enumerate(cols2):
            with col:
                render_card(idx + 6, results[idx + 5]['title'], results[idx + 5])

else:
    st.markdown("""
    <div class="empty-state">
        <div class="empty-state-title">WHAT WILL YOU WATCH?</div>
        <div class="empty-state-sub">SELECT A MOVIE ABOVE AND CLICK FIND MATCHES</div>
    </div>
    """, unsafe_allow_html=True)



