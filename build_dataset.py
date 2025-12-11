import json
import random
import os

# --- Constants & Generators ---

CUISINES = ["Italian", "Mexican", "Asian", "American", "Mediterranean", "Indian", "French", "Thai", "Greek", "Japanese"]
DISH_TYPES = ["Stew", "Stir-fry", "Salad", "Bake", "Soup", "Casserole", "Roast", "Curry", "Pasta", "Tacos", "Burger", "Sandwich", "Bowl"]
ADJECTIVES = ["Spicy", "Savory", "Quick", "Earthy", "Cheesy", "Fresh", "Classic", "Hearty", "Creamy", "Crispy", "Zesty", "Garlicky"]

INGREDIENT_POOL = {
    "Proteins": ["chicken breast", "ground beef", "pork chops", "salmon", "tofu", "shrimp", "eggs", "lentils", "chickpeas", "turkey"],
    "Carbs": ["rice", "pasta", "potatoes", "quinoa", "bread", "tortillas", "noodles", "couscous"],
    "Vegetables": ["tomato", "onion", "garlic", "spinach", "carrot", "broccoli", "bell pepper", "zucchini", "mushrooms", "peas", "corn", "cucumber", "kale", "cauliflower"],
    "Dairy/Fats": ["cheese", "milk", "butter", "olive oil", "heavy cream", "yogurt", "parmesan"],
    "Flavor": ["soy sauce", "lemon", "ginger", "chili powder", "cumin", "paprika", "basil", "oregano", "cilantro", "lime", "honey", "mustard"]
}

def generate_synthetic_recipe(id_counter):
    cuisine = random.choice(CUISINES)
    dish_type = random.choice(DISH_TYPES)
    adj = random.choice(ADJECTIVES)
    
    # Pick ingredients ensuring some logic
    protein = random.choice(INGREDIENT_POOL["Proteins"])
    carb = random.choice(INGREDIENT_POOL["Carbs"])
    veg1 = random.choice(INGREDIENT_POOL["Vegetables"])
    veg2 = random.choice(INGREDIENT_POOL["Vegetables"])
    flavor = random.choice(INGREDIENT_POOL["Flavor"])
    
    while veg1 == veg2:
        veg2 = random.choice(INGREDIENT_POOL["Vegetables"])

    ingredients = [protein, carb, veg1, veg2, flavor, "salt", "pepper"]
    if random.random() > 0.5:
        ingredients.append(random.choice(INGREDIENT_POOL["Dairy/Fats"]))

    title = f"{adj} {cuisine} {protein.capitalize()} {dish_type}"
    
    # Simple logic for veg
    non_veg = ["chicken", "beef", "pork", "salmon", "shrimp", "turkey", "fish"]
    is_veg = not any(meat in protein for meat in non_veg)

    steps = [
        f"Prep: Chop {veg1} and {veg2}.",
        f"Cook: Heat oil and cook {protein} until done.",
        f"Combine: Add {veg1}, {veg2}, and {flavor}.",
        f"Simmer: Cook for 10-15 minutes.",
        f"Serve: Serve hot over {carb}."
    ]

    return {
        "id": id_counter,
        "title": title,
        "ingredients": ingredients,
        "steps": steps,
        "time": random.choice([15, 20, 30, 45, 60]),
        "cuisine": cuisine,
        "veg_bool": is_veg
    }

# --- Normalizers ---

def normalize_forkgasm(data, start_id):
    normalized = []
    recipes = data.get("recipe", [])
    for r in recipes:
        ing_list = []
        # Flatten direct ingredients
        if "ingredient" in r:
            for item in r["ingredient"]:
                if isinstance(item, dict) and "name" in item:
                    ing_list.append(item["name"])
        
        # Flatten groups
        if "ingredientGroup" in r:
            for group in r["ingredientGroup"]:
                if "ingredient" in group:
                    for item in group["ingredient"]:
                        if isinstance(item, dict) and "name" in item:
                            ing_list.append(item["name"])
                            
        # Steps
        steps = []
        if "step" in r:
            for s in r["step"]:
                if "description" in s:
                    steps.append(s["description"])
        
        tags = r.get("tag", [])
        cuisine = "International"
        for t in tags:
            if t in CUISINES:
                cuisine = t
                break
        
        is_veg = "Vegetarian" in tags or "Vegan" in tags
        
        normalized.append({
            "id": start_id + len(normalized),
            "title": r.get("name", "Unknown Recipe"),
            "ingredients": ing_list,
            "steps": steps,
            "time": 45, # Default since not explicit
            "cuisine": cuisine,
            "veg_bool": is_veg
        })
    return normalized

def normalize_dummyjson(data, start_id):
    normalized = []
    recipes = data.get("recipes", [])
    for r in recipes:
        normalized.append({
            "id": start_id + len(normalized),
            "title": r.get("name"),
            "ingredients": r.get("ingredients", []),
            "steps": r.get("instructions", []),
            "time": r.get("cookTimeMinutes", 30) + r.get("prepTimeMinutes", 0),
            "cuisine": r.get("cuisine", "International"),
            "veg_bool": "Vegetarian" in r.get("tags", [])
        })
    return normalized

def main():
    all_recipes = []
    current_id = 1
    
    # 1. Load Forkgasm
    if os.path.exists("data/raw_forkgasm.json"):
        with open("data/raw_forkgasm.json", "r", encoding="utf-8") as f:
            try:
                fg_data = json.load(f)
                norm_fg = normalize_forkgasm(fg_data, current_id)
                all_recipes.extend(norm_fg)
                current_id += len(norm_fg)
                print(f"Loaded {len(norm_fg)} recipes from Forkgasm")
            except Exception as e:
                print(f"Error loading Forkgasm: {e}")

    # 2. Load DummyJSON
    if os.path.exists("data/raw_dummyjson.json"):
        with open("data/raw_dummyjson.json", "r", encoding="utf-8") as f:
            try:
                dj_data = json.load(f)
                norm_dj = normalize_dummyjson(dj_data, current_id)
                all_recipes.extend(norm_dj)
                current_id += len(norm_dj)
                print(f"Loaded {len(norm_dj)} recipes from DummyJSON")
            except Exception as e:
                print(f"Error loading DummyJSON: {e}")

    # 3. Fill the rest with Synthetic
    target_count = 1000
    needed = target_count - len(all_recipes)
    if needed > 0:
        print(f"Generating {needed} synthetic recipes to reach target...")
        for _ in range(needed):
            all_recipes.append(generate_synthetic_recipe(current_id))
            current_id += 1
            
    # Save
    with open("data/recipes.json", "w", encoding="utf-8") as f:
        json.dump(all_recipes, f, indent=4)
    
    print(f"Done! Saved {len(all_recipes)} recipes to data/recipes.json")

if __name__ == "__main__":
    main()
