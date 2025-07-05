from flask import Flask, render_template, request
from math import floor
from jinja2 import Environment

app = Flask(__name__, static_url_path='/static')

# Make Python's built-in functions available in templates
app.jinja_env.globals.update(min=min, max=max)

def calculate_bmi(height, weight):
    """Calculate BMI and return category with health message"""
    try:
        bmi = round(weight / ((height / 100) ** 2), 1)
        
        if bmi < 18.5:
            category = "Underweight"
            message = "Consider consulting a nutritionist"
        elif 18.5 <= bmi < 25:
            category = "Normal weight"
            message = "Maintain your healthy lifestyle"
        elif 25 <= bmi < 30:
            category = "Overweight"
            message = "Consider increasing physical activity"
        else:
            category = "Obese"
            message = "Consult a healthcare provider"
            
        return bmi, category, message
        
    except ZeroDivisionError:
        return None, "Error", "Height cannot be zero"
    except TypeError:
        return None, "Error", "Please enter valid numbers"

@app.route('/', methods=['GET', 'POST'])
def index():
    error = None
    bmi = None
    bmi_category = None
    bmi_message = None
    
    if request.method == 'POST':
        try:
            height = float(request.form.get('height'))
            weight = float(request.form.get('weight'))
            gender = request.form.get('gender', 'male')
            
            if height <= 0 or weight <= 0:
                raise ValueError("Values must be positive")
                
            bmi, bmi_category, bmi_message = calculate_bmi(height, weight)
            
        except ValueError as e:
            error = f"Invalid input: {str(e)}"
        except Exception as e:
            error = f"An error occurred: {str(e)}"
    
    return render_template(
        'index.html',
        error=error,
        bmi=bmi,
        bmi_category=bmi_category,
        bmi_message=bmi_message
    )

if __name__ == '__main__':
    app.run(debug=True)