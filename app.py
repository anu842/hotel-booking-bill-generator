
from flask import Flask, request, render_template_string

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Hotel Booking Bill Generator</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background: #eef2f7;
            padding: 25px;
        }
        .container {
            max-width: 650px;
            margin: auto;
            padding: 25px;
            background: white;
            border-radius: 12px;
            box-shadow: 0 3px 12px #cccccc;
        }
        h1, h2 { text-align: center; color: #234b75; }
        label { display: block; margin-top: 12px; font-weight: bold; }
        input, select {
            width: 100%;
            padding: 10px;
            margin-top: 5px;
            box-sizing: border-box;
        }
        button {
            width: 100%;
            padding: 12px;
            margin-top: 20px;
            background: #234b75;
            color: white;
            border: none;
            border-radius: 5px;
            cursor: pointer;
        }
        .bill {
            background: #e8f5e9;
            padding: 18px;
            margin-top: 22px;
            border-radius: 8px;
        }
        .error { color: red; }
    </style>
</head>
<body>
<div class="container">
    <h1>Hotel Booking Bill Generator</h1>

    <form method="POST">
        <label>Customer Name</label>
        <input type="text" name="customer" required>

        <label>Room Type</label>
        <select name="room_type" required>
            <option value="Standard">Standard</option>
            <option value="Deluxe">Deluxe</option>
            <option value="Suite">Suite</option>
        </select>

        <label>Number of Nights</label>
        <input type="number" name="nights" min="1" required>

        <label>Number of Guests</label>
        <input type="number" name="guests" min="1" required>

        <label>Price per Night (₹)</label>
        <input type="number" name="price" min="0" step="0.01" required>

        <label>Additional Service Charges (₹)</label>
        <input type="number" name="services" min="0" step="0.01" value="0" required>

        <button type="submit">Generate Bill</button>
    </form>

    {% if bill %}
    <div class="bill">
        <h2>Hotel Bill</h2>
        <p><b>Customer:</b> {{ bill.customer }}</p>
        <p><b>Room Type:</b> {{ bill.room_type }}</p>
        <p><b>Nights:</b> {{ bill.nights }}</p>
        <p><b>Guests:</b> {{ bill.guests }}</p>
        <hr>
        <p>Room Charges: ₹{{ "%.2f"|format(bill.room) }}</p>
        <p>Service Charges: ₹{{ "%.2f"|format(bill.services) }}</p>
        <p>Tax Amount (5%): ₹{{ "%.2f"|format(bill.tax) }}</p>
        <h3>Total Bill: ₹{{ "%.2f"|format(bill.total) }}</h3>
        <p>Cost per Guest: ₹{{ "%.2f"|format(bill.per_guest) }}</p>
        <p><b>Booking Category:</b> {{ bill.category }}</p>
    </div>
    {% endif %}

    {% if error %}
    <p class="error">{{ error }}</p>
    {% endif %}
</div>
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def home():
    bill = None
    error = None

    if request.method == "POST":
        try:
            customer = request.form["customer"].strip()
            room_type = request.form["room_type"]
            nights = int(request.form["nights"])
            guests = int(request.form["guests"])
            price = float(request.form["price"])
            services = float(request.form["services"])

            if not customer:
                raise ValueError

            if room_type not in ["Standard", "Deluxe", "Suite"]:
                raise ValueError

            if nights < 1 or guests < 1 or price < 0 or services < 0:
                raise ValueError

            room_charges = nights * price
            tax = (room_charges + services) * 0.05
            total = room_charges + services + tax
            per_guest = total / guests

            if nights <= 2:
                category = "Short Stay"
            elif nights <= 5:
                category = "Regular Stay"
            else:
                category = "Long Stay"

            bill = {
                "customer": customer,
                "room_type": room_type,
                "nights": nights,
                "guests": guests,
                "room": room_charges,
                "services": services,
                "tax": tax,
                "total": total,
                "per_guest": per_guest,
                "category": category
            }

        except (ValueError, KeyError):
            error = "Please enter valid booking details."

    return render_template_string(HTML, bill=bill, error=error)

if __name__ == "__main__":
    app.run(debug=True)
