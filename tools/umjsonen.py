import json
import requests
from phonenumbers import country_code_for_region

with open('tools/all.json', encoding='utf-8') as file:
    input_data = json.load(file)

with open('tools/coverage.json', encoding='utf-8') as file:
    coverage = json.load(file)

with open('tools/drivingside.json', encoding='utf-8') as file:
    drivingside = json.load(file)

output = {}

output['type'] = "FeatureCollection";

features = input_data['features']

new_features = []

for feature in features:
    iso = feature['properties']['iso_a2']

    new_feature = {}
    properties = {}

    try:
        restcountries_url = f"https://restcountries.com/v3.1/alpha/{iso.lower()}"
        restcountries_response = requests.get(restcountries_url)

        if restcountries_response.status_code == 200:
            country_data = restcountries_response.json()

        native_country_names_json = country_data[0]["name"]["nativeName"]
        native_country_names = []

        currencies_json = country_data[0]["currencies"]
        currencies = []

        for a, item in native_country_names_json.items():
            native_country_names.append(item.get("common"))
        
        for a, item in currencies_json.items():
            currencies.append(item.get("name") + " (" +  item.get("symbol") + ")")

        
        native_country_name = ', '.join(native_country_names)
        currency = ', '.join(currencies)

        tld = country_data[0]["tld"]
    except:
        print("nich check")
        native_country_name = ""
        tld = ""
        currency = ""

    properties['name'] = feature['properties']['name']
    properties['iso'] = iso
    properties['tld'] = tld
    properties['native_name'] = native_country_name
    properties['calling_code'] = country_code_for_region(iso)
    properties['rarity'] = coverage[iso.upper()].lower() if iso.upper() in coverage else "no coverage"
    properties['driving'] = drivingside[iso.upper()].lower() if iso.upper() in drivingside else " / "
    properties['currency'] = currency

    new_feature['type'] = "Feature"
    new_feature['properties'] = properties
    new_feature['geometry'] = feature['geometry']

    new_features.append(new_feature)
    print("check")


output['features'] = new_features


with open('tools/data.json', 'w', encoding='utf-8') as output_file:
    json.dump(output, output_file, indent=4)


