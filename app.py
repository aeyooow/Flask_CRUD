from flask import Flask, request, jsonify
import mysql.connector

app = Flask(__name__)

db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'root',
    'database': 'customersandjobsdatamodel',
}

conn = mysql.connector.connect(**db_config)
cursor = conn.cursor()


@app.route('/customers', methods=['GET'])
def get_all_customers():
    try:
        cursor.execute("SELECT * FROM customers")
        customers = cursor.fetchall()
        return jsonify(customers)
    except mysql.connector.Error as err:
        return jsonify({'error': f"Database error: {err}"}), 500

@app.route('/customers/<int:customer_id>', methods=['GET'])
def get_customer(customer_id):
    try:
        cursor.execute("SELECT * FROM customers WHERE customers_id = %s", (customer_id,))
        customer = cursor.fetchone()

        if customer:
            return jsonify(customer)
        else:
            return jsonify({'error': 'Customer not found'}), 404
    except mysql.connector.Error as err:
        return jsonify({'error': f"Database error: {err}"}), 500

@app.route('/customers', methods=['POST'])
def create_customer():
    try:
        data = request.json

        if not all(key in data for key in ['customer_first_name', 'customer_last_name', 'email_address']):
            return jsonify({'error': 'Missing required fields'}), 400

        query = "INSERT INTO customers (customer_first_name, customer_last_name, email_address) VALUES (%s, %s, %s)"
        values = (data['customer_first_name'], data['customer_last_name'], data['email_address'])

        cursor.execute(query, values)
        conn.commit()

        return jsonify({'message': 'Customer created successfully'}), 201
    except mysql.connector.Error as err:
        return jsonify({'error': f"Database error: {err}"}), 500

@app.route('/customers/<int:customer_id>', methods=['PUT'])
def update_customer(customer_id):
    try:
        data = request.json

        if not all(key in data for key in ['customer_first_name', 'customer_last_name', 'email_address']):
            return jsonify({'error': 'Missing required fields'}), 400

        query = "UPDATE customers SET customer_first_name = %s, customer_last_name = %s, email_address = %s WHERE customers_id = %s"
        values = (data['customer_first_name'], data['customer_last_name'], data['email_address'], customer_id)

        cursor.execute(query, values)
        conn.commit()

        return jsonify({'message': 'Customer updated successfully'})
    except mysql.connector.Error as err:
        return jsonify({'error': f"Database error: {err}"}), 500

@app.route('/customers/<int:customer_id>', methods=['DELETE'])
def delete_customer(customer_id):
    try:
        query = "DELETE FROM customers WHERE customers_id = %s"
        values = (customer_id,)

        cursor.execute(query, values)
        conn.commit()

        return jsonify({'message': 'Customer deleted successfully'})
    except mysql.connector.Error as err:
        return jsonify({'error': f"Database error: {err}"}), 500

# Error handling
@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)
