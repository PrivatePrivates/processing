import os
import json
import requests

URL = "http://127.0.0.1:5000"
HEADERS = {'content-type': 'application/json'}

victim_index = 3

base_image = f"victim-{victim_index}-base.jpg"
image_folder_path = f"victim-{victim_index}"

results = []
friend_folders = os.listdir(f"victim-{victim_index}")
for (friend_index, friend) in enumerate(friend_folders):
    print(f"{friend_index+1}/{len(friend_folders)}", friend)
    friend_path = f"{image_folder_path}/{friend}"
    friend_post_files = os.listdir(friend_path)
    if len(friend_post_files) - 2 == 0:
        print("No Location Posts. Skipping!")
        print("\n\n")
        continue
    friend_post_files = list(
        filter(lambda x: x[x.rfind(".")+1:] == "jpg", friend_post_files))
    for (post_index, friend_post) in enumerate(friend_post_files):
        comparison_image = f"{friend_path}/{friend_post}"
        print(f"{post_index+1}/{len(friend_post_files)}", comparison_image)
        request_data = {"image1": base_image, "image2": comparison_image}
        response = requests.post(URL, data=json.dumps(request_data), headers=HEADERS)
        instance_result = {}
        instance_result["username"] = friend
        instance_result["image_path"] = comparison_image
        instance_result["score"] = response.json()["common_features"]
        results.append(instance_result)
    print("\n\n")

sorted_results = sorted(results, key=lambda x: x["score"], reverse=True)

with open(f"results-victim-{victim_index}.json", 'w') as f:
    json.dump(sorted_results, f, indent=4)
