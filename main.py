from flask import Flask, render_template, jsonify, request
import json
import pycountry
from babel import Locale
import langcodes
import requests

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/get-geojson')
def get_geojson():
    with open('selected_countries.geojson') as file:
        geojson_data = json.load(file)
    return geojson_data

@app.route('/trigger-coutry-update', methods=['POST'])
def update_coutry():
    iso = request.json.get('ISO2').lower()
    
    return get_country_data(iso)


def get_country_data(iso) -> json:
    country = pycountry.countries.get(alpha_2=iso)

    restcountries_url = f"https://restcountries.com/v3.1/alpha/{iso.lower()}"
    restcountries_response = requests.get(restcountries_url)

    if restcountries_response.status_code == 200:
        country_data = restcountries_response.json()

    native_country_names = country_data[0]["name"]["nativeName"]
    native_country_name = ""

    for a, item in native_country_names.items():
        native_country_name += item.get("common") + ", "
    

    print(native_country_name)

    flag_url = f"https://flagcdn.com/w640/{iso}.png"

    return jsonify({"flag_url": flag_url,
                    "name": country.name,
                    "native_name": native_country_name
                    })

if __name__ == '__main__':
    app.run(debug=True)
