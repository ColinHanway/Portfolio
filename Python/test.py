import json
import pprint


def generate_json():
    with open("sentinel.json") as jf:
        schema = json.load(jf)

    with open("example_site.json") as jf:
        example = json.load(jf)

    for schema_key in schema["data"]:
        for example_key in example["data"]:
            if example_key == schema_key:
                try:
                    schema[example_key] = example_key[example_key]
                except Exception:
                    schema[example_key] = None

    return schema
