from flask import Flask, render_template_string, request

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Pizza Dough Calculator</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #faf9f6;
            margin: 40px auto;
            max-width: 600px;
            color: #222;
        }
        h1 { color: #a53a1f; text-align: center; }
        form {
            background: #fff;
            padding: 20px;
            border-radius: 12px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }
        label { display: block; margin-top: 10px; font-weight: bold; }
        input, select, button {
            padding: 8px;
            margin-top: 5px;
            width: 100%;
            border-radius: 6px;
            border: 1px solid #ccc;
            box-sizing: border-box;
        }
        button {
            background-color: #38414b;
            color: white;
            border: none;
            font-size: 16px;
            margin-top: 15px;
            cursor: pointer;
        }
        button:hover { background-color: #2b323a; }
        .error {
            color: red;
            background: #f8d7da;
            padding: 10px;
            border-radius: 8px;
            margin-bottom: 10px;
        }
        .result {
            background: #fff;
            padding: 20px;
            border-radius: 12px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            margin-top: 20px;
        }
        ul { list-style-type: none; padding-left: 0; }
        li { margin-bottom: 5px; }
    </style>
</head>
<body>
    <h1>🍞 Pizza Dough Calculator</h1>
    <form method="POST">
        <label>Pizza Size (in inches)</label>
        <input type="number" name="size" step="0.5" min="8" max="24" value="12" required>

        <label>Number of Pizzas</label>
        <input type="number" name="num_pizzas" min="1" value="1" required>

        <label>Pizza Thickness</label>
        <select name="thickness">
            <option value="thin">Thin</option>
            <option value="regular" selected>Regular</option>
            <option value="thick">Thick</option>
        </select>

        <button type="submit">Calculate Dough</button>
    </form>

    {% if error %}
        <div class="error">{{ error }}</div>
    {% endif %}

    {% if result %}
    <div class="result">
        <h2>🍕 Results</h2>
        <p><strong>Target Dough Ball Size:</strong> {{ result['dough_per_pizza']|round }} g each</p>
        <p><strong>Total Dough:</strong> {{ result['total_dough']|round }} g for {{ result['num_pizzas'] }} pizza(s)</p>

        <h3>Ingredients (grams)</h3>
        <ul>
            {% for name, grams in result['ingredients'].items() %}
                <li><strong>{{ name }}:</strong> {{ grams|round(1) }} g</li>
            {% endfor %}
        </ul>
    </div>
    {% endif %}
</body>
</html>
"""

def calculate_pizza_dough(size_in, num_pizzas, thickness):
    if size_in < 10 or size_in > 20:
        return None, "Pizza size must be between 10 and 20 inches."

    base_weight = 187  # grams for 10" regular pizza
    size_factor = (size_in / 10) ** 2
    thickness_factors = {"thin": 0.856, "regular": 1.0, "thick": 1.305}
    t_factor = thickness_factors.get(thickness.lower(), 1.0)

    dough_per_pizza = base_weight * size_factor * t_factor
    total_dough = dough_per_pizza * num_pizzas

    # Baker’s percentages
    flour_ratio = 1 / (1 + 0.620 + 0.0040 + 0.0248 + 0.0203 + 0.0338)
    flour = total_dough * flour_ratio
    water = flour * 0.620
    yeast = flour * 0.0040
    salt = flour * 0.0248
    sugar = flour * 0.0203
    oil = flour * 0.0338

    result = {
        "num_pizzas": num_pizzas,
        "dough_per_pizza": dough_per_pizza,
        "total_dough": total_dough,
        "ingredients": {
            "Bread Flour": flour,
            "Water": water,
            "Yeast": yeast,
            "Salt": salt,
            "Sugar": sugar,
            "Olive Oil": oil
        }
    }

    return result, None

@app.route("/", methods=["GET", "POST"])
def index():
    result, error = None, None
    if request.method == "POST":
        size = float(request.form["size"])
        num_pizzas = int(request.form["num_pizzas"])
        thickness = request.form["thickness"]
        result, error = calculate_pizza_dough(size, num_pizzas, thickness)
    return render_template_string(HTML_TEMPLATE, result=result, error=error)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5080)
