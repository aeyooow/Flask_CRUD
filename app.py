from flask import Flask, request, jsonify
import mysql.connector
import xmltodict

app = Flask(__name__)

# MySQL database connection configuration
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'root',
    'database': 'customersandjobsdatamodel',  # Replace 'your_database_name' with your actual database name
}

# Create MySQL connection
conn = mysql.connector.connect(**db_config)
cursor = conn.cursor()

def convert_to_xml(data, root_name, item_name):
    xml_data = xmltodict.unparse({root_name: {item_name: data}}, full_document=False)
    return xml_data, 200, {'Content-Type': 'application/xml'}

# Customers Routes
@app.route('/customers', methods=['GET'])
def get_all_customers():
    format_type = request.args.get('format', 'json')  # Default to JSON if format not specified
    cursor.execute("SELECT * FROM customers")
    customers = cursor.fetchall()

    if format_type.lower() == 'xml':
        return convert_to_xml(customers, 'customers', 'customer')
    else:
        return jsonify({'customers': customers})

@app.route('/customers/<int:customer_id>', methods=['GET'])
def get_customer(customer_id):
    format_type = request.args.get('format', 'json')  # Default to JSON if format not specified
    cursor.execute("SELECT * FROM customers WHERE customers_id = %s", (customer_id,))
    customer = cursor.fetchone()

    if customer:
        if format_type.lower() == 'xml':
            return convert_to_xml(customer, 'customer', 'customer')
        else:
            return jsonify(customer)
    else:
        return jsonify({'error': 'Customer not found'}), 404

# Jobs Routes
@app.route('/jobs', methods=['GET'])
def get_all_jobs():
    format_type = request.args.get('format', 'json')  # Default to JSON if format not specified
    cursor.execute("SELECT * FROM jobs")
    jobs = cursor.fetchall()

    if format_type.lower() == 'xml':
        return convert_to_xml(jobs, 'jobs', 'job')
    else:
        return jsonify({'jobs': jobs})

@app.route('/jobs/<int:job_id>', methods=['GET'])
def get_job(job_id):
    format_type = request.args.get('format', 'json')  # Default to JSON if format not specified
    cursor.execute("SELECT * FROM jobs WHERE job_id = %s", (job_id,))
    job = cursor.fetchone()

    if job:
        if format_type.lower() == 'xml':
            return convert_to_xml(job, 'job', 'job')
        else:
            return jsonify(job)
    else:
        return jsonify({'error': 'Job not found'}), 404

# Order Items Routes
@app.route('/order_items', methods=['GET'])
def get_all_order_items():
    format_type = request.args.get('format', 'json')  # Default to JSON if format not specified
    cursor.execute("SELECT * FROM order_items")
    order_items = cursor.fetchall()

    if format_type.lower() == 'xml':
        return convert_to_xml(order_items, 'order_items', 'order_item')
    else:
        return jsonify({'order_items': order_items})

# Standard Tasks Routes
@app.route('/standard_tasks', methods=['GET'])
def get_all_standard_tasks():
    format_type = request.args.get('format', 'json')  # Default to JSON if format not specified
    cursor.execute("SELECT * FROM standard_tasks")
    standard_tasks = cursor.fetchall()

    if format_type.lower() == 'xml':
        return convert_to_xml(standard_tasks, 'standard_tasks', 'standard_task')
    else:
        return jsonify({'standard_tasks': standard_tasks})

# Error handling
@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)
