from flask import Flask, render_template, request, redirect, url_for
import json
import os

app = Flask(__name__)

# Path to the JSON file
WORDS_JSON_FILE = 'words.json'

# Load existing data from the JSON file
def load_data():
    # Check if the file exists
    if not os.path.exists(WORDS_JSON_FILE):
        # print(f"Error: {WORDS_JSON_FILE} does not exist.")  # Debug print
        return {}  # Return an empty dictionary if the file doesn't exist
    
    try:
        # Open and read the file
        with open(WORDS_JSON_FILE, 'r') as file:
            data = json.load(file)  # Parse the JSON data
            # print("Loaded data:", data)  # Debug print
            return data
    except json.JSONDecodeError as e:
        # print(f"Error: {WORDS_JSON_FILE} is not valid JSON. Details: {e}")  # Debug print
        return {}  # Return an empty dictionary if the file is not valid JSON

# Save data to the JSON file
def save_data(data):
    with open(WORDS_JSON_FILE, 'w') as file:
        json.dump(data, file, indent=4)

@app.route('/')
def index():
    data = load_data()
    # print("Periods:", list(data.keys()))  # Debug print
    return render_template('index.html', periods=data.keys(), data=data)

@app.route('/add', methods=['POST'])
def add_word():
    period = request.form.get('period')  # Selected period
    word = request.form.get('word')     # Word input
    definition = request.form.get('definition')  # Definition input
    date = request.form.get('date')     # Date input
    word_type = request.form.get('type')  # Type input (E/S/P/FA)

    if period and word and definition and date and word_type:
        data = load_data()
        if period in data:
            # Add the word with its definition, date, and type to the selected period
            data[period][word] = [definition, int(date), word_type]
            save_data(data)  # Save the updated data
    return redirect(url_for('index'))  # Redirect back to the homepage



if __name__ == '__main__':
    app.run(debug=True)