import fastf1
import os

cache_dir = "data/fastf1-cache"
if os.path.exists(cache_dir):
    fastf1.Cache.enable_cache(cache_dir)
    fastf1.Cache.clear_cache(cache_dir)
    print("Cache cleared successfully.")
else:
    print("Cache directory not found or already empty.")
