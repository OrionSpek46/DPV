from flask import Flask, render_template, request, redirect, url_for, flash
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity, set_access_cookies
from models import User, DataModel
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import plotly.express as px
import pandas as pd
import os
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['JWT_TOKEN_LOCATION'] = ['cookies']
app.config['JWT_COOKIE_SECURE'] = False  # Set to True in production with HTTPS
jwt = JWTManager(app)

DATABASE_URI = os.getenv('DATABASE_URI')
engine = create_engine(DATABASE_URI)
Session = sessionmaker(bind=engine)
session = Session()

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = session.query(User).filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            access_token = create_access_token(identity=username)
            response = redirect(url_for('dashboard'))
            set_access_cookies(response, access_token)
            return response
        else:
            flash('Invalid username or password')
            return redirect(url_for('login'))
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        existing_user = session.query(User).filter_by(username=username).first()
        if existing_user:
            flash('Username already exists')
            return redirect(url_for('register'))

        hashed_password = generate_password_hash(password, method='sha256')
        new_user = User(username=username, password=hashed_password)
        session.add(new_user)
        session.commit()
        flash('Registration successful. Please log in.')
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/dashboard')
@jwt_required()
def dashboard():
    # Fetch data from the database
    df = pd.read_sql('processed_data', engine)

    # Create Plotly figures
    fig = px.bar(df, x='category', y='value', title='Data Visualization')

    # Render dashboard template
    return render_template('dashboard.html', graph_json=fig.to_json())

@app.route('/logout')
def logout():
    response = redirect(url_for('login'))
    response.delete_cookie('access_token_cookie')
    flash('You have been logged out.')
    return response

# ... rest of the code ...
