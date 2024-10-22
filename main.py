from flask import Flask, render_template, jsonify, request
import json


with open('static/res/data.json') as data_file:
    data = json.load(data_file)

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/get-geojson')
def get_geojson():
    return data

@app.route('/trigger-country-update', methods=['POST'])
def update_coutry():
    iso = request.json.get('iso')
    return get_country_data(iso)

def get_properties_from_iso(iso):
    for d in data['features']:
        properties = d['properties']
        if properties.get('iso').upper() == str(iso).upper():
            return properties
    return jsonify()


def get_country_data( iso) -> json:
    properties = get_properties_from_iso(iso)

    flag_url = f"https://flagcdn.com/w40/{str(iso).lower()}.png"

    #Plates:
    default_plate = 'static/res/plates/plate.png'
    front_plate = f'static/res/plates/front_{iso}.png'
    back_plate = f'static/res/plates/front_{iso}.png'


    return jsonify({"flag_url": flag_url,
                    "name": properties['name'],
                    "native_name": properties['native_name'],
                    "tld" : properties['tld'],
                    "calling_code" : properties['calling_code'],
                    "driving" : properties['driving'],
                    "currency" : properties['currency'],
                    "plate_path": default_plate
                    })

if __name__ == '__main__':
    app.run(debug=True)
