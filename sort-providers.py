#!/usr/bin/env python3
"""Sort gaterouter.json models: custom provider order, reverse alpha within each group."""

import json

PATH = "internal/providers/configs/gaterouter.json"

PROVIDER_ORDER = {
    "deepseek": 0,
    "anthropic": 1,
    "openai": 2,
    "google": 3,
}

with open(PATH) as f:
    data = json.load(f)

models = data["models"]
auto = [m for m in models if m["id"] == "auto"]
rest = [m for m in models if m["id"] != "auto"]

# Sort by reverse alpha within each group, then by provider priority (stable)
rest.sort(key=lambda m: (PROVIDER_ORDER.get(m["id"].split("/")[0], 4), m["id"]), reverse=True)
rest.sort(key=lambda m: PROVIDER_ORDER.get(m["id"].split("/")[0], 4))

data["models"] = auto + rest

with open(PATH, "w") as f:
    json.dump(data, f, indent=2)
    f.write("\n")
