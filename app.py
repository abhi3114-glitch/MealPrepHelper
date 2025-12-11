import streamlit as st
import json
from typing import List, Dict

# Set page config
st.set_page_config(
    page_title="MealPrepHelper",
    page_icon="🍳",
    layout="wide"
)

# --- Core Logic ---

@st.cache_data
def load_data():
    """Loads recipe data from JSON file."""
    try:
        with open("data/recipes.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        st.error("recipes.json not found. Please run generate_data.py first.")
        return []

def normalize_ingredient(ingredient: str) -> str:
    """Simple normalization for fuzzy matching."""
    return ingredient.lower().strip()

def find_matches(user_ingredients: List[str], recipes: List[Dict]) -> List[Dict]:
    """
    Ranks recipes based on ingredient coverage.
    Returns recipes with match_score attached.
    """
    norm_user_ing = set(normalize_ingredient(i) for i in user_ingredients)
    
    scored_recipes = []
    
    for recipe in recipes:
        recipe_ing = set(normalize_ingredient(i) for i in recipe['ingredients'])
        match_count = 0
        matching_ingredients = []
        missing_ingredients = []
        
        for ring in recipe_ing:
            # Simple substring matching for "fuzzy" effect
            # e.g. "egg" matches "large egg"
            if any(uing in ring or ring in uing for uing in norm_user_ing):
                match_count += 1
                matching_ingredients.append(ring)
            else:
                missing_ingredients.append(ring)
        
        if len(recipe_ing) == 0:
            score = 0
        else:
            score = match_count / len(recipe_ing)
            
        # Only keep recipes with at least one match? 
        # Requirement says "fuzzy match recipes that require subset or small extras"
        # Let's keep if match > 0
        if score > 0:
             # Add computed fields for display
            recipe_copy = recipe.copy()
            recipe_copy['match_score'] = score
            recipe_copy['missing_ingredients'] = missing_ingredients
            recipe_copy['matching_ingredients'] = matching_ingredients
            scored_recipes.append(recipe_copy)
            
    # Sort by match score (desc), then time (asc)
    scored_recipes.sort(key=lambda x: (-x['match_score'], x['time']))
    return scored_recipes

# --- UI Components ---

def inject_custom_css():
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');
        
        /* Global Styles */
        html, body, [class*="css"] {
            font-family: 'Inter', sans-serif;
            background-color: #0E1117;
            color: #FAFAFA;
        }
        
        /* Sidebar */
        [data-testid="stSidebar"] {
            background-color: #161B22;
            border-right: 1px solid #30363D;
        }
        
        /* Headers */
        h1, h2, h3 {
            font-weight: 700 !important;
            color: #FFFFFF !important;
        }
        
        /* Hero Section */
        .hero {
            background: linear-gradient(135deg, #FF4B1F 0%, #1F1C2C 100%);
            padding: 2rem;
            border-radius: 12px;
            margin-bottom: 2rem;
            text-align: center;
            box-shadow: 0 4px 20px rgba(0,0,0,0.4);
        }
        .hero h1 {
            font-size: 3rem !important;
            margin-bottom: 0.5rem;
            text-shadow: 0 2px 4px rgba(0,0,0,0.3);
        }
        .hero p {
            font-size: 1.2rem;
            color: #E0E0E0;
        }

        /* Recipe Card */
        .recipe-card {
            background-color: #1E232B;
            border: 1px solid #30363D;
            border-radius: 12px;
            padding: 1.5rem;
            height: 100%;
            transition: transform 0.2s, box-shadow 0.2s;
        }
        .recipe-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 8px 24px rgba(0,0,0,0.3);
            border-color: #FF4B1F;
        }
        .card-header {
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            margin-bottom: 1rem;
        }
        .match-badge {
            background-color: #238636;
            color: white;
            padding: 4px 8px;
            border-radius: 20px;
            font-size: 0.85rem;
            font-weight: 600;
        }
        .match-badge.partial {
            background-color: #D29922;
        }
        .match-badge.low {
            background-color: #A40E26;
        }
        .card-title {
            font-size: 1.2rem;
            font-weight: 700;
            margin: 0;
            color: #58A6FF;
        }
        .card-meta {
            display: flex;
            gap: 10px;
            margin-bottom: 1rem;
            font-size: 0.9rem;
            color: #8B949E;
        }
        .card-meta span {
            display: flex;
            align-items: center;
            gap: 4px;
        }
        
        /* Input Field */
        .stTextInput input {
            background-color: #0D1117;
            border: 1px solid #30363D;
            color: white;
            border-radius: 8px;
            padding: 0.5rem 1rem;
        }
        .stTextInput input:focus {
            border-color: #58A6FF;
            box-shadow: 0 0 0 2px rgba(88, 166, 255, 0.2);
        }
        
        /* Mobile Responsiveness */
        @media (max-width: 768px) {
            .hero {
                padding: 1.5rem;
                margin-bottom: 1rem;
            }
            .hero h1 {
                font-size: 2rem !important;
            }
            .hero p {
                font-size: 1rem;
            }
            /* Force cards to stack or adjust text on small screens if standard columns squeeze too much */
            .recipe-card {
                padding: 1rem;
            }
            .card-title {
                font-size: 1.1rem;
            }
            .card-meta {
                flex-wrap: wrap; /* allow wrapping on very small phones */
            }
            
            /* Streamlit specific overrides for better mobile spacing */
            .block-container {
                padding-top: 2rem !important;
                padding-left: 1rem !important;
                padding-right: 1rem !important;
            }
            
            /* Force columns to stack on mobile */
            [data-testid="column"] {
                width: 100% !important;
                flex: 1 1 auto !important;
                min-width: 100% !important;
            }
        }
        
        </style>
    """, unsafe_allow_html=True)

def main():
    inject_custom_css()
    
    # Hero Section
    st.markdown("""
        <div class="hero">
            <h1>🍳 MealPrepHelper</h1>
            <p>Turn your fridge into a feast. Enter ingredients, find recipes.</p>
        </div>
    """, unsafe_allow_html=True)

    # Load Data
    recipes = load_data()
    if not recipes:
        return

    # Sidebar Filters
    with st.sidebar:
        st.header("🔍 Filters")
        st.markdown("---")
        
        # Extract all cuisines for filter
        all_cuisines = sorted(list(set(r['cuisine'] for r in recipes)))
        selected_cuisines = st.multiselect("Cuisine", all_cuisines, default=all_cuisines)
        
        max_time = st.slider("Max Time (mins)", min_value=15, max_value=120, value=60, step=15)
        
        diet_filter = st.radio("Preferences", ["All", "Vegetarian Only", "Non-Vegetarian"])
        
        st.markdown("---")
        st.info(f"Loaded **{len(recipes)}** recipes")

    # Main Input
    ingredients_input = st.text_input("What's in your pantry?", "egg, tomato, onion", placeholder="e.g. chicken, rice, garlic")
    
    if ingredients_input:
        user_ingredients = [i.strip() for i in ingredients_input.split(",") if i.strip()]
        
        # Filter Logic
        filtered_recipes = [r for r in recipes if r['cuisine'] in selected_cuisines and r['time'] <= max_time]
        if diet_filter == "Vegetarian Only":
            filtered_recipes = [r for r in filtered_recipes if r['veg_bool']]
        elif diet_filter == "Non-Vegetarian":
            filtered_recipes = [r for r in filtered_recipes if not r['veg_bool']]
            
        # Matching Logic
        matches = find_matches(user_ingredients, filtered_recipes)
        
        st.markdown(f"### 🎯 Found {len(matches)} matches")
        st.write("") # Spacer
        
        if matches:
            # Pagination / Load More
            if 'results_count' not in st.session_state:
                st.session_state.results_count = 12
            
            # Grid Layout
            cols = st.columns(3) # 3 Column Grid
            
            # Display current slice
            visible_matches = matches[:st.session_state.results_count]
            
            for idx, r in enumerate(visible_matches):
                col = cols[idx % 3]
                
                with col:
                    match_pct = int(r['match_score'] * 100)
                    badge_class = "match-badge"
                    if match_pct < 70: badge_class += " partial"
                    if match_pct < 40: badge_class += " low"
                    
                    # HTML Card
                    st.markdown(f"""
                        <div class="recipe-card">
                            <div class="card-header">
                                <div class="card-title">{r['title']}</div>
                                <div class="{badge_class}">{match_pct}% Match</div>
                            </div>
                            <div class="card-meta">
                                <span>⏱ {r['time']}m</span>
                                <span>🌍 {r['cuisine']}</span>
                                <span>{ '🥬 Veg' if r['veg_bool'] else '🍖 Meat' }</span>
                            </div>
                        </div>
                    """, unsafe_allow_html=True)
                    
                    with st.expander("View Details & Shopping List"):
                        st.markdown(f"**Missing:** {', '.join(r['missing_ingredients']) if r['missing_ingredients'] else 'None!'}")
                        st.markdown("**Instructions:**")
                        for i, step in enumerate(r['steps'], 1):
                            st.caption(f"{i}. {step}")

            # Load More Button
            if st.session_state.results_count < len(matches):
                col1, col2, col3 = st.columns([1, 2, 1])
                with col2:
                    if st.button(f"Load More Results ({len(matches) - st.session_state.results_count} remaining)", use_container_width=True):
                        st.session_state.results_count += 12
                        st.rerun()
        else:
            # Reset count if no matches or new search
            st.session_state.results_count = 12

    else:
        st.info("👋 Enter some ingredients above to see magic happen!")

if __name__ == "__main__":
    main()
