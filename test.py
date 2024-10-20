import requests
import json

def save_country_data_to_json(iso2_code, filename):
    """
    Makes a request to the Rest Countries API using the ISO2 code and saves the response to a JSON file.

    Args:
        iso2_code (str): The ISO2 country code (e.g., 'US' for the United States).
        filename (str): The name of the file to save the response to (e.g., 'country_data.json').

    Returns:
        None
    """
    url = f"https://restcountries.com/v3.1/alpha/{iso2_code.lower()}"
    response = requests.get(url)

    if response.status_code == 200:
        # Convert the response to JSON format
        country_data = response.json()
        
        # Save the response to a JSON file
        with open(filename, 'w') as json_file:
            json.dump(country_data, json_file, indent=4)

        print(f"Country data saved to {filename}")
    else:
        print(f"Error: Country code '{iso2_code}' not found.")

# Example usage
iso_code = 'DE'  # Replace with the desired ISO2 country code
filename = 'country_data.json'  # The file where you want to save the data
save_country_data_to_json(iso_code, filename)
