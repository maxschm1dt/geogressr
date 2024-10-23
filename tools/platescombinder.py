import os
from PIL import Image

# Define your directory containing the license plates
directory = 'static/res/plates_raw'
output_directory = 'static/res/plates'

# Create output directory if it doesn't exist
os.makedirs(output_directory, exist_ok=True)

# Loop through the files in the directory
for filename in os.listdir(directory):
    # Check for front plates (assuming file naming convention like 'country_front.jpg' and 'country_back.jpg')
    if 'front' in filename:
        country = filename.split('_')[0]  # Get the country name from the filename
        front_plate_path = os.path.join(directory, filename)
        back_plate_path = os.path.join(directory, f'{country}_back.png')

        # Load the front plate image
        front_plate = Image.open(front_plate_path)

        # Check if the back plate exists
        if os.path.exists(back_plate_path):
            back_plate = Image.open(back_plate_path)
        else:
            print(f"No back plate found for {country}, using front plate twice.")
            back_plate = front_plate

        # Combine the front and back plates side by side
        combined_width = max(front_plate.width, back_plate.width)
        combined_height = front_plate.height + back_plate.height

        combined_image = Image.new('RGB', (combined_width, combined_height))

        # Paste the front plate on top
        combined_image.paste(front_plate, (0, 0))

        # Paste the back plate below the front plate
        combined_image.paste(back_plate, (0, front_plate.height))

        # Save the combined image
        combined_image.save(os.path.join(output_directory, f'{country}.png'))

        print(f"Combined image for {country} saved.")
