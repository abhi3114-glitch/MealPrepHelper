import urllib.request
import json
import os
import time

SOURCES = [
    {
        "name": "gitlab_recipes",
        "url": "https://gitlab.com/datasets/json/recipes/-/raw/master/recipes.json",
        "headers": {"User-Agent": "Mozilla/5.0"}
    },
    {
        "name": "forkgasm",
        "url": "https://raw.githubusercontent.com/LeaVerou/forkgasm/master/recipes.json",
        "headers": {"User-Agent": "Mozilla/5.0"}
    },
    {
        "name": "dummyjson",
        "url": "https://dummyjson.com/recipes?limit=0", # Get total
        "headers": {"User-Agent": "Mozilla/5.0"}
    }
]

def download_file():
    if not os.path.exists("data"):
        os.makedirs("data")

    for source in SOURCES:
        print(f"Downloading {source['name']}...")
        try:
            req = urllib.request.Request(source['url'], headers=source.get('headers', {}))
            with urllib.request.urlopen(req) as response:
                if response.status == 200:
                    data = response.read()
                    with open(f"data/raw_{source['name']}.json", "wb") as f:
                        f.write(data)
                    print(f"✅ Success: {source['name']} ({len(data)} bytes)")
                else:
                    print(f"❌ Failed: {source['name']} Status {response.status}")
        except Exception as e:
            print(f"❌ Error downloading {source['name']}: {e}")
            
if __name__ == "__main__":
    download_file()
