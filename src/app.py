from flask import Flask, render_template, request, flash, redirect, url_for
import json
import os

app = Flask(__name__)
app.secret_key = 'mysecretkey'

# Load product details from a JSON file
def load_products():
    try:
        current_directory = os.path.dirname(os.path.abspath(__file__))
        products_file_path = os.path.join(current_directory, 'products.json')

        with open(products_file_path, 'r') as file:
            products = json.load(file)
    except FileNotFoundError:
        products = []
    return products

# Save product details to a JSON file
def save_products(products):
    try:
        current_directory = os.path.dirname(os.path.abspath(__file__))
        products_file_path = os.path.join(current_directory, 'products.json')

        with open(products_file_path, 'w') as file:
            json.dump(products, file, indent=2)
    except Exception as e:
        print(f"Error saving products: {e}")

# Initialize product_listings as a global variable
product_listings = load_products()

# Route for adding a new product
@app.route('/add_product', methods=['GET', 'POST'])
def add_product():
    global product_listings

    if request.method == 'POST':
        # Retrieve data from the form
        product_name = request.form.get('product_name')
        price_str = request.form.get('price')
        quantity_str = request.form.get('quantity')
        location = request.form.get('location')  # Add this line
        
        print(f"Product Name: {product_name}")
        print(f"Price: {price_str}")
        print(f"Quantity: {quantity_str}")
        print(f"Location: {location}")

        # Check if price, quantity, and location are not empty
        if price_str and quantity_str and location:
            # Convert price and quantity to float and int, respectively
            price = float(price_str)
            quantity = int(quantity_str)

            # Create a dictionary to represent the new product
            new_product = {
                'id': len(product_listings) + 1,
                'name': product_name,
                'cost': price,
                'stocks': quantity,
                'location': location,  # Add this line
            }

            # Append the new product to the list
            product_listings.append(new_product)

            # Save the updated product list to the JSON file
            save_products(product_listings)

            flash('Product added successfully!', 'success')
            return redirect(url_for('home'))

        flash('Invalid input. Please enter valid price, quantity, and location.', 'error')

    return render_template('add_product.html')

# Route for the home page
@app.route('/', methods=['GET', 'POST'])
def home():
    global product_listings

    if request.method == 'POST':
        if 'edit' in request.form:
            return redirect(url_for('edit_product', product_id=request.form['edit']))
        elif 'delete' in request.form:
            product_id = request.form['delete']
            product_listings = [p for p in product_listings if p['id'] != int(product_id)]
            flash('Product deleted successfully!', 'success')
            save_products(product_listings)

    return render_template("home.html", products=product_listings)

# Route for editing a product
@app.route('/edit_product/<product_id>', methods=['GET', 'POST'])
def edit_product(product_id):
    global product_listings

    # Define product in the local scope
    product = next((p for p in product_listings if p['id'] == int(product_id)), None)

    if request.method == 'POST':
        if product:
            # Update the product details based on the form data
            product['name'] = request.form.get('name')
            product['cost'] = float(request.form.get('cost'))
            product['stocks'] = int(request.form.get('stocks'))
            product['location'] = request.form.get('location')  # Add this line
            flash('Product details updated successfully!', 'success')

            # Save updated product details to the JSON file
            save_products(product_listings)
            return redirect(url_for('home'))

    return render_template('edit_product.html', product=product)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
