import json
import os

victim_index = 3

base_image = f"victim-{victim_index}-base.jpg"

with open(f"results-victim-{victim_index}.json") as f:
    results = json.load(f)

top_5 = results[:5]

for image in top_5:
    command = f"cp --parents {image['image_path']} final-demo/"
    os.system(command)
    print(command)
os.system(f"cp {base_image} final-demo/")
os.system(f"cp victim-network-{victim_index}.html final-demo/")