import json
import argparse
from typing import OrderedDict


def load_json(file_path) -> dict:
    with open(file_path, encoding="utf-8") as f:
        return json.load(f)


def restructure_country_codes(scraped_path, ref_path, output_path):
    """
    Restructures country codes data and add ISO A3 codes.
    """
    scraped_country_codes_dict = load_json(scraped_path)
    ref_countries_geojson_dict = load_json(ref_path)

    ref_countries_data = [feature["properties"] for feature in ref_countries_geojson_dict["features"]]

    result_country_codes = {}

    for id, full_name in scraped_country_codes_dict.items():
        result_country_codes[id] = {"full_name": full_name}
        iso_a3 = None
        for ref_country_data in ref_countries_data:
            if ref_country_data["ISO_A2"] == id:
                iso_a3 = ref_country_data["ISO_A3"]
                break
        result_country_codes[id]["iso_a3"] = iso_a3

    result_country_codes = OrderedDict(sorted(result_country_codes.items()))
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(result_country_codes, f, indent=4)


def main():
    parser = argparse.ArgumentParser(description="Restructures country codes data and add ISO A3 codes.")
    parser.add_argument(
        "--scraped",
        default="scripts/data_cleaning/scraped_country_codes.json",
        help="Path to the scraped country codes json file"
    )
    parser.add_argument(
        "--ref",
        default="scripts/data_cleaning/countries.geojson",
        help="Path to the reference countries geojson file"
    )
    parser.add_argument(
        "--output",
        default="scripts/data_cleaning/result_country_codes.json",
        help="Path to the output json file"
    )
    args = parser.parse_args()

    restructure_country_codes(args.scraped, args.ref, args.output)




if __name__ == "__main__":
    main()
