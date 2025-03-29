import os
from flask import Flask, request, render_template
from groq import Groq

app = Flask(__name__)

# Initialize Groq client
grok_client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

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

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        keywords = request.form.get('keywords')
        meal_plan = generate_meal_plan(keywords)
        return render_template('index.html', meal_plan=meal_plan)
    return render_template('index.html', meal_plan=None)

if __name__ == '__main__':
    app.run(debug=True)
