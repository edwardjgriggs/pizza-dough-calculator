from flask import Flask, request, render_template_string

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Pizza Dough Calculator</title>
    <style>
        body { font-family: Arial; background: #fafafa; margin: 50px; }
        input { margin: 5px; padding: 5px; }
        button { padding: 6px 10px; }
    </style>
</head>
<body>
    <h2>Pizza Dough Calculator</h2>
    <form method="post">
        <label>Size (inches):</label>
        <input type="number" name="size_in" step="0.1" required><br>
        <label>Number of pizzas:</label>
        <input type="number" name="num_pizzas" required><br>
        <label>Thickness (thin, regular, thick):</label>
        <input type="text" name="thickness" required><br>
        <button type="submit">Calculate</button>
    </form>
    {% if result %}
        <h3>Result:</h3>
        <p>{{ result }}</p>
    {% endif %}
</body>
</html>
"""

def calculate_pizza_dough(size_in, num_pizzas, thickness):
    base_weight = 187
    size_factor = (size_in / 10) ** 2
    thickness_factors = {"thin": 0.856, "regular": 1.0, "thick": 1.305}
    t_factor = thickness_factors.get(thickness.lower(), 1.0)
    dough_per_pizza = base_weight * size_factor * t_factor
    total_dough = dough_per_pizza * num_pizzas
    return f"Each pizza needs {dough_per_pizza:.1f}g dough. Total: {total_dough:.1f}g."

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
