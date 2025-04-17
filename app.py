from flask import Flask, request, render_template, redirect, url_for, flash
import mysql.connector
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # For flash messages

# MySQL Configuration
db_config = {
    'host': 'localhost',
    'user': 'mango_user',
    'password': 'mango_password',
    #'password': os.getenv('DB_PASSWORD'),
    'database': 'mango_orders'
}

# Route to serve the HTML page
@app.route('/')
def index():
    return render_template('index.html')  # Ensure index.html is in the 'templates' folder

# Route to handle form submissions
@app.route('/submit-order', methods=['POST'])
def submit_order():
    # Debugging: Print the form data
    print(request.form)

    # Retrieve form data
    name = request.form.get('name')
    contact = request.form.get('contact')
    address = request.form.get('address')
    alphonso_quantity = request.form.get('alphonso_quantity', '0')
    ratnagiri_quantity = request.form.get('ratnagiri_quantity', '0')
    kesar_quantity = request.form.get('kesar_quantity', '0')

    # Debugging: Print the retrieved values
    print(f"Name: {name}, Contact: {contact}, Address: {address}")
    print(f"Alphonso: {alphonso_quantity}, Ratnagiri: {ratnagiri_quantity}, Kesar: {kesar_quantity}")

    # Connect to the database
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()

    # Insert the order into the database
    query = """
        INSERT INTO orders (name, contact, address, alphonso_quantity, ratnagiri_quantity, kesar_quantity)
        VALUES (%s, %s, %s, %s, %s, %s)
    """
    values = (name, contact, address, alphonso_quantity, ratnagiri_quantity, kesar_quantity)
    cursor.execute(query, values)
    connection.commit()

    # Close the connection
    cursor.close()
    connection.close()

    # Flash a thank-you message
    flash("Thank you for your order! We will contact you soon.")

    # Redirect to the thank-you page
    return redirect(url_for('thank_you'))

@app.route('/view-orders', methods=['GET', 'POST'])
def view_orders():
    # Hardcoded admin credentials
    admin_credentials = {
        'username': 'admin',  # Replace with your desired admin username
        'password': 'password'  # Replace with your desired admin password
    }

    if request.method == 'POST':
        # Get the username and password from the form
        username = request.form.get('username')
        password = request.form.get('password')

        # Debugging: Print the submitted username and password
        print(f"Submitted Username: {username}, Submitted Password: {password}")

        # Validate the credentials
        if username == admin_credentials['username'] and password == admin_credentials['password']:
            try:
                # Connect to the database
                connection = mysql.connector.connect(**db_config)
                cursor = connection.cursor(dictionary=True)

                # Fetch all orders
                cursor.execute("SELECT * FROM orders")
                orders = cursor.fetchall()

                # Debugging: Print the fetched orders
                print(f"Fetched Orders: {orders}")

            except mysql.connector.Error as err:
                print(f"Error: {err}")
                orders = []
            finally:
                if 'cursor' in locals():
                    cursor.close()
                if 'connection' in locals():
                    connection.close()

            # Render the orders page
            return render_template('view_orders.html', orders=orders)
        else:
            # Flash an error message if credentials are invalid
            flash("Invalid username or password. Access denied.")
            return redirect(url_for('view_orders'))

    # Render the login form for the admin
    return render_template('admin_login.html')

@app.route('/thank-you')
def thank_you():
    return render_template('thank_you.html')  # Ensure thank_you.html is in the 'templates' folder

if __name__ == '__main__':
    app.run(debug=True)