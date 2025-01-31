from flask import Flask, request, jsonify
import sqlite3  # Or your preferred database library

app = Flask(__name__)

# Create the database (if it doesn't exist)
def create_database():
    conn = sqlite3.connect('countries.db')  # Database file
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS countries (
            name TEXT PRIMARY KEY,
            capital TEXT,
            population INTEGER,
            area INTEGER,
            currency TEXT
            -- Add other facts as needed
        )
    ''')
    # Example data (you'll likely want to populate this from a file or API)
    c.execute("INSERT OR IGNORE INTO countries (name, capital, population, area, currency) VALUES ('Austria', 'Vienna', 9000000, 83879, 'EUR')")
    c.execute("INSERT OR IGNORE INTO countries (name, capital, population, area, currency) VALUES ('Belgium', 'Brussels', 11500000, 30528, 'EUR')")
    c.execute("INSERT OR IGNORE INTO countries (name, capital, population, area, currency) VALUES ('Bulgaria', 'Sofia', 7000000, 110879, 'BGN')")
    c.execute("INSERT OR IGNORE INTO countries (name, capital, population, area, currency) VALUES ('France', 'Paris', 65000000, 640679, 'EUR')")
    c.execute("INSERT OR IGNORE INTO countries (name, capital, population, area, currency) VALUES ('Germany', 'Berlin', 83000000, 357022, 'EUR')")
    c.execute("INSERT OR IGNORE INTO countries (name, capital, population, area, currency) VALUES ('Greece', 'Athens', 10500000, 131957, 'EUR')")
    c.execute("INSERT OR IGNORE INTO countries (name, capital, population, area, currency) VALUES ('Italy', 'Rome', 60000000, 301340, 'EUR')")
    c.execute("INSERT OR IGNORE INTO countries (name, capital, population, area, currency) VALUES ('Spain', 'Madrid', 47000000, 505990, 'EUR')")
    c.execute("INSERT OR IGNORE INTO countries (name, capital, population, area, currency) VALUES ('Sweden', 'Stockholm', 10000000, 450295, 'SEK')")
    conn.commit()
    conn.close()

create_database() # Create on startup


@app.route('/get_country_facts', methods=['POST'])
def get_country_facts():
    data = request.get_json()
    country = data.get('country')

    try:
        conn = sqlite3.connect('countries.db')
        c = conn.cursor()
        c.execute("SELECT * FROM countries WHERE name = ?", (country,))
        facts = c.fetchall()
        conn.close()
        if facts:
            # Convert list of tuples to list of dictionaries for easier JSON handling
            column_names = [description[0] for description in c.description]
            facts_list = [dict(zip(column_names, row)) for row in facts]

            return jsonify(facts_list) # Return as JSON
        else:
            return jsonify({'error': 'Country not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500  # Handle errors


if __name__ == '__main__':
    app.run(debug=True) # Set debug=False in production
