#!/usr/bin/python3

import os
import json
from pathlib import Path

# generate config.json for VITE-Deployment
output_path = Path("/usr/share/nginx/html/ui/config.json")

vite_env_vars = {key: value for key, value in os.environ.items() if key.startswith("VITE_")}

output_path.parent.mkdir(parents=True, exist_ok=True)

with open(output_path, "w") as f:
    json.dump(vite_env_vars, f, indent=2)

print(f"Written {len(vite_env_vars)} VITE_ variables to {output_path}")
