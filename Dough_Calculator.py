import streamlit as st

def calculate_pizza_dough(size_in, num_pizzas, thickness):
    # --- Check for valid size ---
    if size_in < 10 or size_in > 20:
        st.error("⚠️ Sorry, that pizza size is out of range (10–20 inches).")
        return

    # --- Base settings ---
    base_weight = 187  # grams, 10" regular pizza
    size_factor = (size_in / 10) ** 2
    thickness_factors = {"thin": 0.856, "regular": 1.0, "thick": 1.305}
    t_factor = thickness_factors.get(thickness.lower(), 1.0)

    # --- Dough weight ---
    dough_per_pizza = base_weight * size_factor * t_factor
    total_dough = dough_per_pizza * num_pizzas

    # --- Baker's percentages ---
    flour_ratio = 1 / (1 + 0.620 + 0.0040 + 0.0248 + 0.0203 + 0.0338)
    flour = total_dough * flour_ratio
    water = flour * 0.620
    yeast = flour * 0.0040
    salt = flour * 0.0248
    sugar = flour * 0.0203
    oil = flour * 0.0338

    # --- Results ---
    st.subheader("🍕 Results")
    st.write(f"**Target Dough Ball Size:** {dough_per_pizza:.0f} g each")
    st.write(f"**Total Dough:** {total_dough:.0f} g for {num_pizzas} pizza(s)")

    st.markdown("### Ingredients (grams)")
    st.write(f"- Bread Flour: **{flour:.0f} g**")
    st.write(f"- Water: **{water:.0f} g**")
    st.write(f"- Yeast: **{yeast:.1f} g**")
    st.write(f"- Salt: **{salt:.0f} g**")
    st.write(f"- Sugar: **{sugar:.0f} g**")
    st.write(f"- Olive Oil: **{oil:.0f} g**")


# --- Streamlit UI ---
st.title("🍞 Pizza Dough Calculator")

size = st.number_input("Pizza Size (in inches)", min_value=8.0, max_value=24.0, value=12.0, step=0.5)
qty = st.number_input("Number of Pizzas", min_value=1, value=1, step=1)
thickness = st.radio("Pizza Thickness", ["thin", "regular", "thick"])

if st.button("Calculate Dough"):
    calculate_pizza_dough(size, qty, thickness)
