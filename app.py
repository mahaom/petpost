# app.py
import os
import json
import boto3
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# --- AWS S3 Configuration ---
# !!! IMPORTANT: REPLACE 'YOUR_BUCKET_NAME' WITH YOUR ACTUAL S3 BUCKET NAME !!!
S3_BUCKET = 'YOUR_BUCKET_NAME'
S3_REGION = 'us-east-1' # Change if your bucket is in a different region
s3 = boto3.client('s3', region_name=S3_REGION)
PETS_DATA_FILE = 'pets.json'

def get_pet_data():
    """Reads pet data from the JSON file."""
    if not os.path.exists(PETS_DATA_FILE):
        return []
    with open(PETS_DATA_FILE, 'r') as f:
        return json.load(f)

def save_pet_data(data):
    """Saves pet data to the JSON file."""
    with open(PETS_DATA_FILE, 'w') as f:
        json.dump(data, f, indent=4)

@app.route('/')
def index():
    """Displays the list of adoptable pets."""
    pets = get_pet_data()
    return render_template('index.html', pets=pets)

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    """Handles the pet upload form."""
    if request.method == 'POST':
        # 1. Get form data
        name = request.form['name']
        age = request.form['age']
        breed = request.form['breed']
        image = request.files['image']

        if image:
            # 2. Upload image to S3
            filename = image.filename
            s3.upload_fileobj(
                image,
                S3_BUCKET,
                filename,
                ExtraArgs={'ACL': 'public-read', 'ContentType': image.content_type}
            )
            # 3. Construct the public image URL
            image_url = f"https://{S3_BUCKET}.s3.amazonaws.com/{filename}"

            # 4. Save new pet data
            pets = get_pet_data()
            pets.append({
                'name': name,
                'age': age,
                'breed': breed,
                'image_url': image_url
            })
            save_pet_data(pets)

        # 5. Redirect to the homepage
        return redirect(url_for('index'))

    # If GET request, just show the form
    return render_template('upload.html')

if __name__ == '__main__':
    # Running on 0.0.0.0 makes it accessible from the public IP
    app.run(host='0.0.0.0', port=80, debug=True)