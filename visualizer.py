from pandas.io.formats.format import EngFormatter
from pyvis.network import Network
import json
import pandas

GOLD_COLOR = "#D4AF37"
IMAGE_BLUE = "#00AEEF"
USER_GREEN = "#8CC63F"
VICTIM_RED = "#B20838"

# victim_index = 1
# victim_name = "________j17"

# victim_index = 2
# victim_name = "muntahatoor"

victim_index = 3
victim_name = "marilenadance"

with open(f"results-victim-{victim_index}.json") as f:
    results = json.load(f)

with open(f"victim-data/{victim_name}/followee.txt") as f:
    friends = f.readlines()

friends = set(list(map(lambda x: x.strip(), friends))[:150])
location_friends = set(map(lambda x: x["username"], results))
friends.update(location_friends)

top_5_friends = set(map(lambda x: x["username"], results[:5]))
top_5_images = set(map(lambda x: x["image_path"], results[:5]))

get_link = lambda text, link : f"<a href=\'{link}' target=\'_blank\'>{text}</a>"

net = Network(height="1200", width="2600px")

# net.add_node(victim_name, color=VICTIM_RED, shape="circle", title="<a href=\'http://www.google.com\' target=\'_blank\'>google</a>")
net.add_node(victim_name, color=VICTIM_RED, title=get_link(victim_name, f"victim-{victim_index}-base.jpg"), label=" ")

for friend in friends:
    net.add_node(friend, size=15, color=USER_GREEN, title=friend, label=" ")
    net.add_edge(friend, victim_name, color= GOLD_COLOR if friend in top_5_friends else USER_GREEN)

for image in results:
    is_top_5 = image["image_path"] in top_5_images
    
    with open(f"victim-{victim_index}/{image['username']}/metadata.csv") as f:
        metadata = f.readlines()

    image_name = image["image_path"][image["image_path"].rfind('/')+1:-4].strip()
    location = ""
    for i in range(len(metadata)-4):
        if i % 5 == 0:
            entry_name = metadata[i+4][len("imagename,"):].strip()
            # print(entry_name, image_name)
            if entry_name == image_name:
                location = metadata[i + 2]
                # print(i, entry_name, )
                break

    if location == "":
        print(image_name, location)
    
    net.add_node(image["image_path"], title=get_link(location, image["image_path"]) if is_top_5 else image["image_path"], color=GOLD_COLOR if is_top_5 else IMAGE_BLUE, label=" ")
    net.add_edge(image["image_path"], image["username"], color= GOLD_COLOR if is_top_5 else USER_GREEN)


net.show(f"victim-network-{victim_index}.html")
