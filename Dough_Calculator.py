from flask import Flask, request, render_template_string

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Pizza Dough Calculator</title>
    <style>
        body { font-family: Arial, sans-serif; background: #1b1b1b; color: #eee; text-align: center; padding: 40px; }
        input, select, button { margin: 6px; padding: 8px; font-size: 16px; border-radius: 6px; border: none; }
        button { background-color: #e63946; color: white; cursor: pointer; }
        button:hover { background-color: #b12d37; }
        .result { margin-top: 25px; font-size: 18px; }
    </style>
</head>
<body>
    <h1>🍕 Pizza Dough Calculator</h1>
    <form method="post">
        <label>Pizza Size (inches):</label><br>
        <input type="number" name="size_in" step="0.1" required><br>

        <label>Number of Pizzas:</label><br>
        <input type="number" name="num_pizzas" required><br>

        <label>Thickness:</label><br>
        <select name="thickness" required>
            <option value="thin">Thin</option>
            <option value="regular">Regular</option>
            <option value="thick">Thick</option>
        </select><br><br>

        <button type="submit">Calculate</button>
    </form>

    {% if result %}
    <div class="result">{{ result }}</div>
    {% endif %}
</body>
</html>
"""

def calculate_pizza_dough(size_in, num_pizzas, thickness):
    base_weight = 187  # grams for 10" regular pizza
    size_factor = (size_in / 10) ** 2
    thickness_factors = {"thin": 0.856, "regular": 1.0, "thick": 1.305}
    t_factor = thickness_factors.get(thickness.lower(), 1.0)
    dough_per_pizza = base_weight * size_factor * t_factor
    total_dough = dough_per_pizza * num_pizzas
    oz_per_pizza = dough_per_pizza / 28.35
    total_oz = total_dough / 28.35
    return f"Each pizza: {dough_per_pizza:.1f}g ({oz_per_pizza:.1f} oz) — Total: {total_dough:.1f}g ({total_oz:.1f} oz)"

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    if request.method == "POST":
        size_in = float(request.form["size_in"])
        num_pizzas = int(request.form["num_pizzas"])
        thickness = request.form["thickness"]
        result = calculate_pizza_dough(size_in, num_pizzas, thickness)
    return render_template_string(HTML, result=result)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5080)
