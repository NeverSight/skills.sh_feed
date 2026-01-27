import json

p = "data/skills.json"

with open(p, "r", encoding="utf-8") as f:
    data = json.load(f)

all_time = data.get("allTime", [])
trending = data.get("trending", [])
hot = data.get("hot", [])

unique = {
    (s.get("source"), s.get("skillId"))
    for s in (all_time + trending + hot)
}

print("allTime", len(all_time))
print("trending", len(trending))
print("hot", len(hot))
print("sum", len(all_time) + len(trending) + len(hot))
print("unique_across_all_arrays", len(unique))
