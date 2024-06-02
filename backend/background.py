from flask import Flask, request, jsonify, send_from_directory, render_template

app = Flask(__name__)

# Hardcoded example packages
packages = [
    {
        "id": "pkg1",
        "image": "img/package-1.jpg",
        "location": "Thailand",
        "duration": "3 days",
        "people": "2 Person",
        "rating": "4.5",
        "reviews": "250",
        "price": "350",
        "startDate": "20/10/2024"
    },
    {
        "id": "pkg2",
        "image": "img/package-2.jpg",
        "location": "Morocco",
        "duration": "1 week",
        "people": "4 Person",
        "rating": "4.8",
        "reviews": "300",
        "price": "800",
        "startDate": "15/11/2024"
    },    
    {
        "id": "pkg2",
        "image": "img/package-2.jpg",
        "location": "Morocco",
        "duration": "1 week",
        "people": "4 Person",
        "rating": "4.8",
        "reviews": "300",
        "price": "800",
        "startDate": "15/11/2024"
    },
    # Add more packages as needed
]

# Dictionary to track the current values of the booking bar arguments
booking_bar_values = {
    "region": set(),
    "departure": set(),
    "duration": set(),
    "price": set(),
    "month": set()
}

@app.route('/get_packages', methods=['POST'])
def get_packages():
    data = request.json



    region = data.get('region')
    departure = data.get('departure')
    duration = data.get('duration')
    price = data.get('price')
    month = data.get('month')


    # Update the dictionary with the current values
    booking_bar_values["region"].add(region)
    booking_bar_values["departure"].add(departure)
    booking_bar_values["duration"].add(duration)
    booking_bar_values["price"].add(price)
    booking_bar_values["month"].add(month)

    print("Current booking bar values:", booking_bar_values)


    
    filtered_packages = [pkg for pkg in packages]  # Simple example, implement actual filtering logic

    if region == "1":
        filtered_packages = filtered_packages[:1]
    if region == "2":
        filtered_packages = filtered_packages[:2]

    return jsonify(filtered_packages)

@app.route('/' )
def index():
    return render_template('index.html')

@app.route('/package.html')
def package():
    return render_template('package.html')

@app.route('/<path:path>', methods=['GET'])
def serve_static(path):
    return send_from_directory('static', path)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
