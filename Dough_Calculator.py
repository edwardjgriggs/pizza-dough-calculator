from flask import Flask, request, render_template_string

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html>
<head>
  <title>Pizza Dough Calculator</title>
</head>
<body>
  <h1>Pizza Dough Calculator</h1>
  <form method="POST">
    <label>Pizza Size (in inches): </label><input type="number" name="size_in" required><br><br>
    <label>Number of Pizzas: </label><input type="number" name="num_pizzas" required><br><br>
    <label>Thickness: </label>
    <select name="thickness">
      <option value="thin">Thin</option>
      <option value="regular">Regular</option>
      <option value="thick">Thick</option>
    </select><br><br>
    <input type="submit" value="Calculate">
  </form>
  {% if result %}
    <h2>Total Dough Needed: {{ result }} grams</h2>
  {% endif %}
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def home():
    result = None
    if request.method == "POST":
        size_in = float(request.form["size_in"])
        num_pizzas = int(request.form["num_pizzas"])
        thickness = request.form["thickness"]

        base_weight = 187  # grams for 10" regular pizza
        size_factor = (size_in / 10) ** 2
        thickness_factors = {"thin": 0.856, "regular": 1.0, "thick": 1.305}
        t_factor = thickness_factors.get(thickness.lower(), 1.0)

        dough_per_pizza = base_weight * size_factor * t_factor
        total_dough = round(dough_per_pizza * num_pizzas, 2)
        result = total_dough
    return render_template_string(HTML, result=result)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
