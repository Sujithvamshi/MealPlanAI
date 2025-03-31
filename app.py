import os
from flask import Flask, request, render_template, jsonify
from groq import Groq
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
# Initialize Groq client
grok_client = Groq(api_key="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")

def generate_meal_plan(keywords):
    prompt = (
        f"Generate a detailed weekly meal plan in table format for a healthy diet based on these keywords: {keywords}.\n"
        "Each day from Sunday to Saturday should include Breakfast, Lunch, and Dinner.\n"
        "Ensure variety and nutritional balance. Format the response as follows:\n"
        "| Day       | Breakfast                                      | Lunch                                          | Dinner                                          |\n"
        "|-----------|----------------------------------------------|----------------------------------------------|----------------------------------------------|\n"
        "| Sunday    | <Meal>                                      | <Meal>                                      | <Meal>                                      |\n"
        "| Monday    | <Meal>                                      | <Meal>                                      | <Meal>                                      |\n"
        "| Tuesday   | <Meal>                                      | <Meal>                                      | <Meal>                                      |\n"
        "| Wednesday | <Meal>                                      | <Meal>                                      | <Meal>                                      |\n"
        "| Thursday  | <Meal>                                      | <Meal>                                      | <Meal>                                      |\n"
        "| Friday    | <Meal>                                      | <Meal>                                      | <Meal>                                      |\n"
        "| Saturday  | <Meal>                                      | <Meal>                                      | <Meal>                                      |\n"
    )
    
    chat_completion = grok_client.chat.completions.create(
        messages=[{"role": "user", "content": prompt}],
        model="llama-3.3-70b-versatile",
    )
    
    return chat_completion.choices[0].message.content

def parse_meal_plan(text):
    lines = text.split('\n')[2:]
    meal_plan = {}
    for line in lines:
        parts = [p.strip() for p in line.split('|') if p.strip()]
        if len(parts) == 4:
            day, breakfast, lunch, dinner = parts
            meal_plan[day] = {
                "breakfast": breakfast,
                "lunch": lunch,
                "dinner": dinner
            }
    return meal_plan

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        keywords = request.form.get('keywords')
        meal_plan = generate_meal_plan(keywords)
        return render_template('index.html', meal_plan=meal_plan)
    return render_template('index.html', meal_plan=None)

@app.route('/api/meal-plan', methods=['POST'])
def api_meal_plan():
    keywords = request.json.get('keywords', '')
    meal_plan_text = generate_meal_plan(keywords)
    meal_plan_json = parse_meal_plan(meal_plan_text)
    return jsonify(meal_plan_json)

if __name__ == '__main__':
    app.run(debug=True)