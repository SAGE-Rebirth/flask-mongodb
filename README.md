# Flask & MongoDB Integration

## Table of Contents
1. [Creating a Free MongoDB Cluster](#creating-a-free-mongodb-cluster)
2. [Configuring Database Access](#configuring-database-access)
3. [Setting Up Network Access](#setting-up-network-access)
4. [Setting Up Flask](#setting-up-flask)
5. [Running the Flask Application](#running-the-flask-application)
6. [Bonus & Notes](#bonus--notes)

## Creating a Free MongoDB Cluster
1. Go to MongoDB Atlas and create a new cluster.
2. Choose the **free plan**, provide a **unique name** for the cluster.
3. Select a cloud provider (**AWS, Azure, or GCP**) and choose a region (e.g., **Mumbai (ap-south-1)**).
4. Click **Create** to finalize the setup.

## Configuring Database Access
1. Create a **new database** and provide a **unique name**.
2. Add a **collection name** (must be unique as well).
3. Add a **user** for authentication.
4. If you haven't created a user, create one now.

### Setting Up Database Access
1. Navigate to **Security > Database Access**.
2. Click **Add New Database User**.
3. Choose an authentication method (**password-based** authentication recommended).
4. Enter a **username and password** (save them for later use).
5. Assign a **role** with **Read & Write Access**.

### Bonus & Notes
- You can **add a temporary database user** for limited-time access (**6 hours - 1 week**).

## Setting Up Network Access
1. Go to **Security > Network Access > IP Access List**.
2. Click **Add IP Address**.
3. Add your **current IP address**.

### Bonus:
- You can **add temporary IP addresses** for limited-time access.
- For learning purposes, you can set **0.0.0.0/0** (Allows access from anywhere).
- A faster way is using **Security > Quickstart**, where you’ll find all necessary options.

## Setting Up Flask
### Installing Required Packages
1. Install dependencies using:
   ```sh
   pip install -r requirements.txt
   ```
2. Alternatively, create a virtual environment and install dependencies:
   ```sh
   python -m venv flask-app-env
   flask-app-env\Scripts\activate  # Windows
   pip install -r requirements.txt
   ```

### Configuring Environment Variables
Create a **.env** file and add the following details:
```sh
MONGO_URI= "Enter your MongoDB Connection String"
MONGO_DB_NAME= "Enter Database Name"
MONGO_COLLECTION_NAME= "Enter Collection Name"
SECRET_KEY= "Enter your Secret Key (Random Alpha-Numeric)"
```

#### Notes:
- **SECRET_KEY** is used for session management, encryption, and CSRF protection.
- Rename **sample.env** to **.env** before running the application.

## Running the Flask Application
Run the application using one of the following commands:
```sh
flask run
```
OR
```sh
python app.py
```

---
This guide ensures a smooth integration of **Flask with MongoDB** for your application. 🚀
You can contribute to this demo app, submit PRs 👍