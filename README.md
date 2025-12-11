# MealPrepHelper

MealPrepHelper is a standalone Streamlit web application designed to suggest recipes based on available household ingredients. It operates entirely offline using a local dataset of over 1000 recipes, ranking suggestions by ingredient match percentage and preparation time.

## Project Goal
To provide a lightweight, privacy-focused tool that helps users reduce food waste by finding practical recipes for ingredients they already possess.

## Features

### Ingredient Matching
- Accepts a comma-separated list of ingredients (e.g., "egg, tomato, onion").
- Uses a fuzzy matching algorithm to identify relevant recipes.
- Ranks results by match score (how many user ingredients found vs. total recipe ingredients).

### Advanced Filtering
- **Cuisine**: Filter by categories such as Italian, Mexican, Asian, and Mediterranean.
- **Dietary Preferences**: Options for Vegetarian Only, Non-Vegetarian, or All diets.
- **Preparation Time**: Slider control to filter recipes by maximum time required (15-120 minutes).

### Interactive UI
- **Dark Mode Design**: Features a modern dark interface with a responsive grid layout.
- **Mobile Optimized**: Fully responsive layout that stacks content vertically on smaller screens.
- **Pagination**: "Load More" functionality to efficiently browse through large sets of search results.
- **Shopping List**: Automatically identifies missing ingredients for selected recipes.

## Technical Details

- **Frontend**: Streamlit (Python)
- **Data Source**: Local JSON database (`data/recipes.json`) containing 1000+ entries, aggregated from open-source datasets and high-quality synthetic data.
- **Algorithm**: Custom Python logic for text normalization, set-based matching, and scoring.

## Installation and Setup

1. **Clone the Repository**
   ```bash
   git clone https://github.com/abhi3114-glitch/MealPrepHelper.git
   cd MealPrepHelper
   ```

2. **Install Dependencies**
   Ensure you have Python installed. Then run:
   ```bash
   pip install -r requirements.txt
   ```

3. **Data Generation (Optional)**
   The project comes with pre-generated data. To regenerate or expand the dataset:
   ```bash
   python build_dataset.py
   ```

4. **Run the Application**
   ```bash
   streamlit run app.py
   ```
   The application will launch in your default web browser at `http://localhost:8501`.

## Project Structure

- `app.py`: Main application logic and UI rendering.
- `build_dataset.py`: Script to download, normalize, and generate the recipe dataset.
- `requirements.txt`: Python package dependencies.
- `data/`: Directory containing the JSON recipe database.

## License
This project is open source and available under the MIT License.
