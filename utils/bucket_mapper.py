import json
from pathlib import Path


class BucketMapper:

    def __init__(self):

        config_path = (
            Path(__file__).parent.parent
            / "config"
            / "bucket_mapping.json"
        )

        with open(config_path, "r") as f:
            self.mapping = json.load(f)

    def enrich(self, result: dict):

        bucket = result.get("primary_bucket")

        mapping = self.mapping.get(bucket)

        if mapping:

            result["complexity"] = mapping["complexity"]
            result["urgency"] = mapping["urgency"]

        return result