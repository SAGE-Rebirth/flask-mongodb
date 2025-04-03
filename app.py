from flask import Flask, render_template, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, DateField, SubmitField
from wtforms.validators import DataRequired, Email, Length, Regexp
from werkzeug.security import generate_password_hash
from pymongo import MongoClient
from dotenv import load_dotenv
import os
import logging
from flask_paginate import Pagination, get_page_args
import certifi

load_dotenv()  # Load environment variables from .env file

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "default_secret_key")  # Secure secret key

# MongoDB Configuration
mongo_uri = os.getenv("MONGO_URI")
# print(mongo_uri)  # Debugging line to check the MongoDB URI

mongo_db_name = os.getenv("MONGO_DB_NAME")
# print(mongo_db_name)  # Debugging line to check the MongoDB database name

# SSL Configuration
# ca_file_path = os.path.join(os.path.dirname(__file__), 'global-bundle.pem')

try:
    # Option 1: Using your downloaded CA file
    # mongo_client = MongoClient(
    #     mongo_uri,
    #     tlsCAFile=ca_file_path
    # )
    
    # Option 2: Using certifi's CA bundle (alternative)
    mongo_client = MongoClient(
        mongo_uri,
        tlsCAFile=certifi.where()
    )
    
    db = mongo_client[mongo_db_name]
    users_collection = db[os.getenv("MONGO_COLLECTION_NAME")]
    # print(users_collection)  # Debugging line to check the MongoDB collection
    
    # Test the connection
    mongo_client.admin.command('ping')
    logging.info("Successfully connected to MongoDB with SSL!")
except Exception as e:
    logging.error(f"Error connecting to MongoDB: {e}")
    raise  # This will stop the app if connection fails

# Form Definition
class UserForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired(), Length(min=2, max=50)])
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=6)])
    dob = DateField("Date of Birth", validators=[DataRequired()], format='%Y-%m-%d')
    contact = StringField("Contact", validators=[
        DataRequired(), Regexp(r'^\+?\d{10,15}$', message="Invalid contact number.")
    ])
    submit = SubmitField("Submit")

@app.route("/", methods=["GET", "POST"])
def index():
    form = UserForm()
    message = None  # Variable to hold success or error messages
    if form.validate_on_submit():
        try:
            # Hash the password
            hashed_password = generate_password_hash(form.password.data)
            
            # Prepare user data
            user_data = {
                "name": form.name.data,
                "email": form.email.data,
                "password": hashed_password,  # Store the hashed password
                "dob": form.dob.data.strftime('%Y-%m-%d'),
                "contact": form.contact.data
            }
            
            # Check for duplicate email
            if users_collection.find_one({"email": user_data["email"]}):
                message = "Email already exists! Please use a different email."
                return render_template("form.html", form=form, message=message)
            
            # Insert into MongoDB
            users_collection.insert_one(user_data)
            message = "User data submitted successfully!"
        except Exception as e:
            logging.error(f"Error inserting user data: {e}")
            message = "An error occurred while submitting data. Please try again."
        return render_template("form.html", form=form, message=message)
    
    return render_template("form.html", form=form, message=message)

@app.route("/delete_all", methods=["POST"])
def delete_all():
    try:
        users_collection.delete_many({})  # Delete all documents in the collection
        message = "All user entries have been deleted successfully!"
        logging.info(message)
    except Exception as e:
        message = "An error occurred while deleting user entries."
        logging.error(f"Error deleting user entries: {e}")
    return render_template("form.html", form=UserForm(), message=message)

@app.route("/users", methods=["GET"])
def users():
    try:
        # Pagination setup
        page, per_page, offset = get_page_args(page_parameter="page", per_page_parameter="per_page")
        per_page = 10  # Items per page
        total = users_collection.count_documents({})
        all_users = users_collection.find({}).skip(offset).limit(per_page)
        
        # No decryption needed for passwords
        users_list = list(all_users)
        
        pagination = Pagination(page=page, per_page=per_page, total=total, css_framework="bootstrap4")
        return render_template("users.html", users=users_list, pagination=pagination, back_url=url_for("index"))
    except Exception as e:
        logging.error(f"Error fetching users: {e}")
        return render_template("users.html", users=[], pagination=None, error="An error occurred while fetching users.", back_url=url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)
