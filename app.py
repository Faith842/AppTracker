print("🚀 app.py is running...")

from flask import Flask, render_template, request, redirect, url_for, session
import requests

app = Flask(__name__)
app.secret_key = 'your-secret-key'

@app.route('/', methods=['GET', 'POST'])
def index():
    if 'meals' not in session:
        session['meals'] = []

    if request.method == 'POST':
        food_item = request.form.get('food')
        if food_item:
            url = f"https://api.calorieninjas.com/v1/nutrition?query={food_item}"
            response = requests.get(url, headers={'X-Api-Key': 'YOUR_API_KEY'})
            if response.status_code == 200:
                data = response.json()
                if data['items']:
                    item = data['items'][0]
                    meal = {
                        'name': item['name'],
                        'calories': item.get('calories', 0),
                        'protein': item.get('protein_g', 0),
                        'carbs': item.get('carbohydrates_total_g', 0),
                        'fat': item.get('fat_total_g', 0)
                    }
                    session['meals'].append(meal)
                    session.modified = True
        return redirect(url_for('index'))

    return render_template('index.html', meals=session['meals'])

@app.route('/summary')
def summary():
    totals = {
        'calories': sum(m['calories'] for m in session.get('meals', [])),
        'protein': sum(m['protein'] for m in session.get('meals', [])),
        'carbs': sum(m['carbs'] for m in session.get('meals', [])),
        'fat': sum(m['fat'] for m in session.get('meals', []))
    }
    return render_template('summary.html', totals=totals)

@app.route('/reset')
def reset():
    session.pop('meals', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
