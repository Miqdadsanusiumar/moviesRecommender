import pickle
import streamlit as st
import requests
import pandas as pd
import numpy as np

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

.movie-card {
    position: relative;
    border-radius: 12px;
    overflow: hidden;
    background: #1a1a1a;
    margin-bottom: 1.5rem;
    transition: transform 0.3s ease, box-shadow 0.3s ease;
    border: 1px solid #2a2a2a;
    height: 100%;
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
}
.movie-info {
    padd
