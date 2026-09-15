import json

from pathlib import Path
import sys
source_path = Path(__file__).resolve()
source_dir = source_path.parent

class settings:
    compact = []
    base_url = ""
    default_model = ""
    compact_default = {}

    def __init__(self):
        with open(f"{source_dir}/settings.json", "r") as file:
            data_json = file.read()
        data = json.loads(data_json)

        self.compact = data["compact_thresholds"]
        self.base_url = data["base_url"]
        self.default_model = data["default_model"]
        self.compact_default = data["compact_default"]
        
    def get_compact_threshold(self, ctx_size):
        for setting in self.compact:
            applicable = False

            if setting["when"] == "above" and ctx_size >= setting["size"]:
                applicable = True
            if setting["when"] == "below" and ctx_size <= setting["size"]:
                applicable = True
            if setting["when"] == "exactly" and ctx_size == setting["size"]:
                applicable = True

            if applicable:
                if setting["type"] == "value":
                    return setting["threshold"]
                elif setting["type"] == "percent":
                    # Multiplier = threshold / 100
                    # returned = ctx_size * Multiplier
                    return round(ctx_size * (setting["threshold"] / 100))
                else:
                    print(f"WARNING: Invalid compact threshold type '{setting["type"]}', skipping")

        # This is just a copy of what's above, mostly
        setting = self.compact_default
        if setting["type"] == "value":
            return setting["threshold"]
        elif setting["type"] == "percent":
            return round(ctx_size * (setting["threshold"] / 100))
        else:
            print(f"WARNING: Invalid default compact threshold type '{setting["type"]}'. Using hardcoded default of 2000.")
            return 2000