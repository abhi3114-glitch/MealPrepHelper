import json
import random

# Sample data pools
INGREDIENTS = [
    "egg", "chicken", "rice", "pasta", "tomato", "potato", "onion", "garlic", "cheese",
    "bread", "milk", "butter", "carrot", "beef", "pork", "fish", "spinach", "flour",
    "sugar", "salt", "pepper", "olive oil", "soy sauce", "lemon", "ginger", "chili"
]

CUISINES = ["Italian", "Mexican", "Asian", "American", "Mediterranean", "Indian"]
ADJECTIVES = ["Spicy", "Savory", "Quick", "Earthy", "Cheesy", "Fresh", "Classic", "Hearty"]
TYPES = ["Stew", "Stir-fry", "Salad", "Bake", "Soup", "Casserole", "Roast", "Toast", "Omelet"]

def generate_recipe(id):
    # Randomly select 3-8 ingredients
    num_ingredients = random.randint(3, 8)
    recipe_ingredients = random.sample(INGREDIENTS, num_ingredients)
    
    # Generate title
    main_ingredient = recipe_ingredients[0].capitalize()
    cuisine = random.choice(CUISINES)
    title = f"{random.choice(ADJECTIVES)} {cuisine} {main_ingredient} {random.choice(TYPES)}"
    
    # Determine veg
    non_veg_items = ["chicken", "beef", "pork", "fish"]
    is_veg = not any(item in recipe_ingredients for item in non_veg_items)
    
    return {
        "id": id,
        "title": title,
        "ingredients": recipe_ingredients,
        "steps": [
            f"Chop {recipe_ingredients[0]} and {recipe_ingredients[1]}.",
            "Heat pan and add oil.",
            "Cook ingredients for 10 minutes.",
            "Serve hot."
        ],
        "time": random.choice([15, 30, 45, 60, 90]),
        "cuisine": cuisine,
        "veg_bool": is_veg
    }

def main():
    recipes = [generate_recipe(i) for i in range(1, 251)] # Generate 250 recipes
    
    with open("data/recipes.json", "w") as f:
        json.dump(recipes, f, indent=4)
    
    print(f"Generated {len(recipes)} recipes in data/recipes.json")

if __name__ == "__main__":
    import os
    os.makedirs("data", exist_ok=True)
    main()
