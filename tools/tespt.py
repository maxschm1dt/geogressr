import phonenumbers
from phonenumbers import country_code_for_region

# Function to get calling code by country (ISO 3166-1 alpha-2 country code)
def get_calling_code(country_code):
    try:
        return country_code_for_region(country_code.upper())
    except:
        return "Invalid country code"

# Example usage
country = "US"  # ISO 3166-1 country code
calling_code = get_calling_code(country)
print(f"The calling code for {country} is: +{calling_code}")

# Test with other countries
print(f"The calling code for India (IN) is: +{get_calling_code('in')}")
print(f"The calling code for UK (GB) is: +{get_calling_code('gb')}")
print(f"The calling code for France (FR) is: +{get_calling_code('fr')}")
