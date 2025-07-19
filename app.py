import uuid

from flask import Flask, render_template, request, redirect
import boto3, os, json
from werkzeug.utils import secure_filename

app = Flask(__name__)
S3_BUCKET = 'petpost-images-bucket'  # Replace this
DATA_FILE = 'pets.json'

s3 = boto3.client('s3')

# Load pets from JSON file
def load_pets():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, 'r') as f:
        return json.load(f)

# Save pets to JSON file
def save_pets(pets):
    with open(DATA_FILE, 'w') as f:
        json.dump(pets, f)

@app.route('/')
def index():
    pets = load_pets()
    breed_filter = request.args.get('breed')
    age_filter = request.args.get('age')

    if breed_filter:
        pets = [p for p in pets if p['breed'].lower() == breed_filter.lower()]
    if age_filter:
        pets = [p for p in pets if p['age'] == age_filter]

    return render_template('index.html', pets=pets)

@app.route('/edit/<pet_id>', methods=['GET', 'POST'])
def edit(pet_id):
    pets = load_pets()
    pet = next((p for p in pets if p['id'] == pet_id), None)
    if not pet:
        return "Pet not found"

    if request.method == 'POST':
        pet['name'] = request.form['name']
        pet['age'] = request.form['age']
        pet['breed'] = request.form['breed']
        save_pets(pets)
        return redirect('/')

    return render_template('edit.html', pet=pet)

@app.route('/delete/<pet_id>', methods=['POST'])
def delete(pet_id):
    pets = load_pets()
    pets = [p for p in pets if p['id'] != pet_id]
    save_pets(pets)
    return redirect('/')


@app.route('/upload', methods=['POST'])
def upload():
    try:
        name = request.form['name']
        age = request.form['age']
        breed = request.form['breed']
        photo = request.files['photo']

        if photo.filename == '':
            return 'No file selected'

        filename = secure_filename(photo.filename)
        s3.upload_fileobj(photo, S3_BUCKET, filename)
        image_url = f"https://{S3_BUCKET}.s3.amazonaws.com/{filename}"

       # pet = {'name': name, 'age': age, 'breed': breed, 'image': image_url}

        pet = {
            'id': str(uuid.uuid4()),  # ✅ NEW LINE
            'name': name,
            'age': age,
            'breed': breed,
            'image': image_url
        }

        
        # Create pets.json if not exists
        if not os.path.exists(DATA_FILE):
            with open(DATA_FILE, 'w') as f:
                json.dump([], f)

        pets = load_pets()
        pets.append(pet)
        save_pets(pets)

        return redirect('/')
    
    except Exception as e:
        return f"An error occurred: {e}"

    
   # return redirect('/')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
