from flask import Flask, render_template, request, flash, redirect, url_for
import json 

# Create Flask app instance
app = Flask(__name__)
app.secret_key = 'mysecretkey'

# Create an empty list to store property listings
property_listings = []

# Route for homepage
@app.route('/')
def home():
    return render_template("home.html", property_listings=property_listings)

# Route to Buy property
@app.route('/buy_property', methods=['GET', 'POST'])
def buy_property():
    if request.method == 'POST':
        property_name = request.form.get('property_name')
        property_type = request.form.get('property_type')
        budget = request.form.get('budget')
        message = request.form.get('message')
        
        # Create a dictionary to represent the property listing
        property_listing = {
            'property_name': property_name,
            'property_type': property_type,
            'budget': budget,
            'message': message,
        }
        
        # Append the property listing to the list
        property_listings.append(property_listing)
        
        flash('Property purchase request submitted successfully!', 'success')
        return redirect(url_for('home'))
    return render_template('buy_property.html')

# Route to sell property
@app.route('/sell_property', methods=['GET', 'POST'])
def sell_property():
    if request.method == 'POST':
        property_name = request.form.get('property_name')
        property_type = request.form.get('property_type')
        rent = request.form.get('rent')
        description = request.form.get('description')
        
        # Create a dictionary to represent the property listing
        property_listing = {
            'property_name': property_name,
            'property_type': property_type,
            'rent': rent,
            'description': description,
        }
        
        # Append the property listing to the list
        property_listings.append(property_listing)
        
        flash('Property listing submitted successfully!', 'success')
        return redirect(url_for('home'))
    return render_template('sell_property.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

