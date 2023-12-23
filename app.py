from flask import Flask, request, jsonify
import mysql.connector
import xmltodict

app = Flask(__name__)

# MySQL database connection configuration
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'root',
    'database': 'customersandjobsdatamodel',  
}

# Create MySQL connection
conn = mysql.connector.connect(**db_config)
cursor = conn.cursor()

def convert_to_xml(data, root_name, item_name):
    xml_data = xmltodict.unparse({root_name: {item_name: data}}, full_document=False)
    return xml_data, 200, {'Content-Type': 'application/xml'}

# CRUD operations for customers

@app.route('/customers', methods=['GET'])

def get_all_customers():
    cursor.execute("SELECT * FROM customers")
    customers = cursor.fetchall()
    return jsonify({'customers': customers})

@app.route('/customers/<int:customer_id>', methods=['GET'])

def get_customer(customer_id):
    cursor.execute("SELECT * FROM customers WHERE customers_id = %s", (customer_id,))
    customer = cursor.fetchone()

    if customer:
        return jsonify({'customer': customer})
    else:
        return jsonify({'error': 'Customer not found'}), 404

@app.route('/customers', methods=['POST'])

def create_customer():
    data = request.json

    if not all(key in data for key in ['customer_first_name', 'customer_last_name', 'email_address']):
        return jsonify({'error': 'Missing required fields'}), 400

    query = """
    INSERT INTO customers 
    (customer_first_name, customer_middle_initial, customer_last_name, gender, email_address, 
    phone_number, address_line_1, address_line_2, address_line_3, address_line_4, 
    town_city, state_country_province, country, other_details) 
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    
    values = (
        data['customer_first_name'], data.get('customer_middle_initial', ''),
        data['customer_last_name'], data.get('gender', ''),
        data['email_address'], data.get('phone_number', ''),
        data.get('address_line_1', ''), data.get('address_line_2', ''),
        data.get('address_line_3', ''), data.get('address_line_4', ''),
        data.get('town_city', ''), data.get('state_country_province', ''),
        data.get('country', ''), data.get('other_details', '')
    )

    cursor.execute(query, values)
    conn.commit()

    return jsonify({'message': 'Customer created successfully'}), 201

@app.route('/customers/<int:customer_id>', methods=['PUT'])

def update_customer(customer_id):
    data = request.json

    if not all(key in data for key in ['customer_first_name', 'customer_last_name', 'email_address']):
        return jsonify({'error': 'Missing required fields'}), 400

    query = """
    UPDATE customers 
    SET 
    customer_first_name = %s, 
    customer_middle_initial = %s,
    customer_last_name = %s, 
    gender = %s, 
    email_address = %s, 
    phone_number = %s, 
    address_line_1 = %s, 
    address_line_2 = %s, 
    address_line_3 = %s, 
    address_line_4 = %s, 
    town_city = %s, 
    state_country_province = %s, 
    country = %s, 
    other_details = %s
    WHERE customers_id = %s
    """
    
    values = (
        data['customer_first_name'], data.get('customer_middle_initial', ''),
        data['customer_last_name'], data.get('gender', ''),
        data['email_address'], data.get('phone_number', ''),
        data.get('address_line_1', ''), data.get('address_line_2', ''),
        data.get('address_line_3', ''), data.get('address_line_4', ''),
        data.get('town_city', ''), data.get('state_country_province', ''),
        data.get('country', ''), data.get('other_details', ''),
        customer_id
    )

    cursor.execute(query, values)
    conn.commit()

    return jsonify({'message': 'Customer updated successfully'})

@app.route('/customers/<int:customer_id>', methods=['DELETE'])

def delete_customer(customer_id):
    query = "DELETE FROM customers WHERE customers_id = %s"
    values = (customer_id,)

    cursor.execute(query, values)
    conn.commit()

    return jsonify({'message': 'Customer deleted successfully'})

# CRUD operations for jobs

@app.route('/jobs', methods=['GET'])

def get_all_jobs():
    cursor.execute("SELECT * FROM jobs")
    jobs = cursor.fetchall()
    return jsonify({'jobs': jobs})

@app.route('/jobs/<int:job_id>', methods=['GET'])

def get_job(job_id):
    cursor.execute("SELECT * FROM jobs WHERE job_id = %s", (job_id,))
    job = cursor.fetchone()

    if job:
        return jsonify({'job': job})
    else:
        return jsonify({'error': 'Job not found'}), 404

@app.route('/jobs', methods=['POST'])

def create_job():
    data = request.json

    if not all(key in data for key in ['date_job_started', 'date_job_completed']):
        return jsonify({'error': 'Missing required fields'}), 400

    query = """
    INSERT INTO jobs (date_job_started, date_job_completed, other_details, customers_customers_id) 
    VALUES (%s, %s, %s, %s)
    """

    values = (
        data['date_job_started'], data['date_job_completed'],
        data.get('other_details', ''), data.get('customers_customers_id', '')
    )

    cursor.execute(query, values)
    conn.commit()

    return jsonify({'message': 'Job created successfully'}), 201

@app.route('/jobs/<int:job_id>', methods=['PUT'])

def update_job(job_id):
    data = request.json

    if not all(key in data for key in ['date_job_started', 'date_job_completed']):
        return jsonify({'error': 'Missing required fields'}), 400

    query = """
    UPDATE jobs 
    SET 
    date_job_started = %s, 
    date_job_completed = %s, 
    other_details = %s, 
    customers_customers_id = %s
    WHERE job_id = %s
    """

    values = (
        data['date_job_started'], data['date_job_completed'],
        data.get('other_details', ''), data.get('customers_customers_id', ''),
        job_id
    )

    cursor.execute(query, values)
    conn.commit()

    return jsonify({'message': 'Job updated successfully'})

@app.route('/jobs/<int:job_id>', methods=['DELETE'])

def delete_job(job_id):
    query = "DELETE FROM jobs WHERE job_id = %s"
    values = (job_id,)

    cursor.execute(query, values)
    conn.commit()

    return jsonify({'message': 'Job deleted successfully'})

# CRUD operations for order_items

@app.route('/order_items', methods=['GET'])

def get_all_order_items():
    cursor.execute("SELECT * FROM order_items")
    order_items = cursor.fetchall()
    return jsonify({'order_items': order_items})

@app.route('/order_items/<int:order_item_id>', methods=['GET'])

def get_order_item(order_item_id):
    cursor.execute("SELECT * FROM order_items WHERE order_item_id = %s", (order_item_id,))
    order_item = cursor.fetchone()

    if order_item:
        return jsonify({'order_item': order_item})
    else:
        return jsonify({'error': 'Order item not found'}), 404

@app.route('/order_items', methods=['POST'])

def create_order_item():
    data = request.json

    if not all(key in data for key in ['quantity', 'cost']):
        return jsonify({'error': 'Missing required fields'}), 400

    query = """
    INSERT INTO order_items (quantity, cost, other_details, jobs_job_id, standard_tasks_task_id) 
    VALUES (%s, %s, %s, %s, %s)
    """

    values = (
        data['quantity'], data['cost'],
        data.get('other_details', ''), data.get('jobs_job_id', ''), data.get('standard_tasks_task_id', '')
    )

    cursor.execute(query, values)
    conn.commit()

    return jsonify({'message': 'Order item created successfully'}), 201

@app.route('/order_items/<int:order_item_id>', methods=['PUT'])

def update_order_item(order_item_id):
    data = request.json

    if not all(key in data for key in ['quantity', 'cost']):
        return jsonify({'error': 'Missing required fields'}), 400

    query = """
    UPDATE order_items 
    SET 
    quantity = %s, 
    cost = %s, 
    other_details = %s, 
    jobs_job_id = %s, 
    standard_tasks_task_id = %s
    WHERE order_item_id = %s
    """

    values = (
        data['quantity'], data['cost'],
        data.get('other_details', ''), data.get('jobs_job_id', ''), data.get('standard_tasks_task_id', ''),
        order_item_id
    )

    cursor.execute(query, values)
    conn.commit()

    return jsonify({'message': 'Order item updated successfully'})

@app.route('/order_items/<int:order_item_id>', methods=['DELETE'])

def delete_order_item(order_item_id):
    query = "DELETE FROM order_items WHERE order_item_id = %s"
    values = (order_item_id,)

    cursor.execute(query, values)
    conn.commit()

    return jsonify({'message': 'Order item deleted successfully'})

# CRUD operations for standard_tasks

@app.route('/standard_tasks', methods=['POST'])

def create_standard_task():
    data = request.json

    if not all(key in data for key in ['task_name', 'task_price', 'task_description']):
        return jsonify({'error': 'Missing required fields'}), 400

    query = """
    INSERT INTO standard_tasks (task_name, task_price, task_description, other_details) 
    VALUES (%s, %s, %s, %s)
    """

    values = (
        data['task_name'], data['task_price'],
        data.get('task_description', ''), data.get('other_details', '')
    )

    cursor.execute(query, values)
    conn.commit()

    return jsonify({'message': 'Standard task created successfully'}), 201

@app.route('/standard_tasks/<int:task_id>', methods=['PUT'])

def update_standard_task(task_id):
    data = request.json

    if not all(key in data for key in ['task_name', 'task_price', 'task_description']):
        return jsonify({'error': 'Missing required fields'}), 400

    query = """
    UPDATE standard_tasks 
    SET 
    task_name = %s, 
    task_price = %s, 
    task_description = %s, 
    other_details = %s
    WHERE task_id = %s
    """

    values = (
        data['task_name'], data['task_price'],
        data.get('task_description', ''), data.get('other_details', ''),
        task_id
    )

    cursor.execute(query, values)
    conn.commit()

    return jsonify({'message': 'Standard task updated successfully'})

@app.route('/standard_tasks/<int:task_id>', methods=['DELETE'])

def delete_standard_task(task_id):
    query = "DELETE FROM standard_tasks WHERE task_id = %s"
    values = (task_id,)

    cursor.execute(query, values)
    conn.commit()

    return jsonify({'message': 'Standard task deleted successfully'})

# Error handling
@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500
    
if __name__ == '__main__':
    # Start the Flask application
    app.run(debug=True)