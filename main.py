from flask import Flask, render_template, jsonify, request
import json
import os


with open('static/res/data.json') as data_file:
    data = json.load(data_file)

app = Flask(__name__)

def get_path_if_exists(path):
    return "static/res/empty.png" if not os.path.exists(path) else path

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

    plate_path = get_path_if_exists(f'static/res/plates/{iso}.png')

    #europe: warn & zebra / otherwise stop & ?
    sign_1 = get_path_if_exists(f'static/res/signs/{iso}_1.png')
    sign_2 = get_path_if_exists(f'static/res/signs/{iso}_2.png')

    roadmarks = get_path_if_exists(f'static/res/road/{iso}_road.png')

    utility_poles = get_path_if_exists(f'static/res/road/{iso}_pole.png')

    extra_1 = get_path_if_exists(f'static/res/extra/{iso}_1.png')
    extra_2 = get_path_if_exists(f'static/res/extra/{iso}_2.png')
    extra_3 = get_path_if_exists(f'static/res/extra/{iso}_3.png')
    extra_4 = get_path_if_exists(f'static/res/extra/{iso}_4.png')

    #markdowns:
    detail_path = f"static/res/htmls/{str(iso).lower()}.html"
    detail = ""

    if os.path.exists(detail_path):
        with open(detail_path, encoding='UTF-8') as detail_file:
            detail = detail_file.read()


    return jsonify({"flag_url": flag_url,
                    "iso" : iso,
                    "name": properties['name'],
                    "native_name": properties['native_name'],
                    "tld" : properties['tld'],
                    "calling_code" : properties['calling_code'],
                    "driving" : properties['driving'],
                    "currency" : properties['currency'],
                    "plate_path": plate_path,
                    "sign_1_path" : sign_1,
                    "sign_2_path" : sign_2,
                    "roadmarks_path" : roadmarks,
                    "utility_poles_path" : utility_poles,
                    "extra_1_path" : extra_1,
                    "extra_2_path" : extra_2,
                    "extra_3_path" : extra_3,
                    "extra_4_path" : extra_4,
                    "detail" : detail
                    })

if __name__ == '__main__':
    app.run(debug=True)
