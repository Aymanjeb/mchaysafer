from flask import Flask, request, jsonify, render_template, send_file
import mysql.connector
import csv
from io import StringIO, BytesIO

app = Flask(__name__)

def get_db_connection():
    return mysql.connector.connect(
        host='db',
        user='root',
        password='password',
        database='offers_db'
    )

@app.route('/')
def form():
    return render_template('form.html')

@app.route('/submit', methods=['POST'])
def submit_form():
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO offers (link_to_offer, description, price, title, date, duration, starting_location, 
                            destination_region, provider_name, provider_phone_number, discount_flag, 
                            price_before_disc, discount_rate, included_services, not_included_services, 
                            locations_per_day, activities_per_day, additional_information, image_links) 
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """, (data['link_to_offer'], data['description'], data['price'], data['title'], data['date'], 
          data['duration'], data['starting_location'], data['destination_region'], data['provider_name'], 
          data['provider_phone_number'], data['discount_flag'], data['price_before_disc'], data['discount_rate'], 
          data['included_services'], data['not_included_services'], data['locations_per_day'], data['activities_per_day'], 
          data['additional_information'], data['image_links']))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'status': 'success'}), 201

@app.route('/offers', methods=['GET'])
def get_offers():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM offers")
    offers = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(offers), 200

@app.route('/offers/<int:id>', methods=['PUT'])
def update_offer(id):
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE offers SET link_to_offer=%s, description=%s, price=%s, title=%s, date=%s, duration=%s, 
                          starting_location=%s, destination_region=%s, provider_name=%s, provider_phone_number=%s, 
                          discount_flag=%s, price_before_disc=%s, discount_rate=%s, included_services=%s, 
                          not_included_services=%s, locations_per_day=%s, activities_per_day=%s, 
                          additional_information=%s, image_links=%s 
        WHERE id=%s
    """, (data['link_to_offer'], data['description'], data['price'], data['title'], data['date'], 
          data['duration'], data['starting_location'], data['destination_region'], data['provider_name'], 
          data['provider_phone_number'], data['discount_flag'], data['price_before_disc'], data['discount_rate'], 
          data['included_services'], data['not_included_services'], data['locations_per_day'], data['activities_per_day'], 
          data['additional_information'], data['image_links'], id))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'status': 'success'}), 200

@app.route('/offers/<int:id>', methods=['DELETE'])
def delete_offer(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM offers WHERE id=%s", (id,))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'status': 'success'}), 200

@app.route('/download', methods=['GET'])
def download_offers():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM offers")
    offers = cursor.fetchall()
    cursor.close()
    conn.close()

    output = StringIO()
    writer = csv.writer(output)
    writer.writerow(['ID', 'Link to Offer', 'Description', 'Price', 'Title', 'Date', 'Duration', 'Starting Location', 
                     'Destination Region', 'Provider Name', 'Provider Phone Number', 'Discount Flag', 
                     'Price Before Discount', 'Discount Rate', 'Included Services', 'Not Included Services', 
                     'Locations per Day', 'Activities per Day', 'Additional Information', 'Image Links'])
    
    for offer in offers:
        writer.writerow(offer)
    
    output.seek(0)
    output_binary = BytesIO(output.getvalue().encode('utf-8'))
    
    return send_file(output_binary, mimetype='text/csv', download_name='offers.csv', as_attachment=True)

if __name__ == '__main__':
    app.run(host='0.0.0.0')
