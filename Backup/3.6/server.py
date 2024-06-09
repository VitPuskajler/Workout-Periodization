from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, session, flash, request, jsonify
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase,sessionmaker, mapper
from sqlalchemy.exc import IntegrityError
from sqlalchemy import Integer, String, Float, Column, inspect, create_engine, text, insert, MetaData, Table
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, IntegerField, FloatField, SubmitField
from wtforms.validators import DataRequired, EqualTo, NumberRange
from werkzeug.security import generate_password_hash, check_password_hash
import re

NOW = datetime.now()
DATE = NOW.strftime("%d%m%Y")

app = Flask(__name__)
app.secret_key = "thiskeyshouldntbeherebutfornowitisok.1084"

# Login manager setup
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

# Database setup
class Base(DeclarativeBase):
    pass

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///workout_plan_01.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Create engine so I can work with dynamic tables
engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])

db = SQLAlchemy(model_class=Base)

db.init_app(app)

class User(UserMixin, db.Model):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String(100), unique=True, nullable=False)
    password = Column(String(100), nullable=False)
    age = Column(Integer, unique=False, nullable=False)
    weight = Column(Float, nullable=False)
    mesocycles = Column(Integer, nullable=True)

    def __init__(self, username, password, age, weight):
        self.username = username
        self.password = password
        self.age = age
        self.weight = weight
        

    def __repr__(self):
        return f'<User {self.username}>'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class WorkoutPlan(db.Model):
    id = db.Column(db.String, primary_key=True)
    exercise = db.Column(db.String(100), nullable=False)
    sets = db.Column(db.Integer, nullable=False)
    pauses = db.Column(db.Integer, nullable=False)
    first_set = db.Column(db.Integer)
    weight_first_set = db.Column(db.Float)
    rpe_first_set = db.Column(db.Float)
    second_set = db.Column(db.Integer)
    weight_second_set = db.Column(db.Float)
    rpe_second_set = db.Column(db.Float)
    third_set = db.Column(db.Integer)
    weight_third_set = db.Column(db.Float)
    rpe_third_set = db.Column(db.Float)
    notes = db.Column(db.String)

    def __repr__(self):
        return f"<WorkoutPlan {self.excercise}>"

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired(), EqualTo('confirm', message='Passwords must match')])
    confirm = PasswordField('Confirm Password')
    age = IntegerField('Age', validators=[DataRequired(), NumberRange(min=0)])
    weight = FloatField('Weight', validators=[DataRequired(), NumberRange(min=0)])
    submit = SubmitField('Sign Up')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Sign In')

# ----------------------------------------------------------------------------------------------

# Function to reflect a table
def reflect_table(table_name, engine):
    metadata = MetaData()
    metadata.bind = engine
    reflected_table = Table(table_name, metadata, autoload_with=engine)
    return reflected_table

# Function to create a dynamic ORM model
def create_dynamic_model(table_name, engine):
    class DynamicTableModel:
        pass

    reflected_table = reflect_table(table_name, engine)
    mapper(DynamicTableModel, reflected_table)
    return DynamicTableModel    

def fetch_dynamic_table_data(table_name, engine):
    # Create the dynamic model for the specified table
    DynamicModel = create_dynamic_model(table_name, engine)

    # Create a session
    Session = sessionmaker(bind=engine)
    session = Session()

    # Query the table
    results = session.query(DynamicModel).all()

    # Convert results to dictionaries
    data = [row.__dict__ for row in results]

    # Remove SQLAlchemy internal key
    for item in data:
        item.pop('_sa_instance_state', None)

    return data

@app.route('/dynamic_table_data/<table_name>')
@login_required
def dynamic_table_data(table_name):
    try:
        data = fetch_dynamic_table_data(table_name, engine)
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)})

@app.route('/fetch_data')
@login_required
def fetch_data():
    # Example: Fetch the current user's dynamically created table
    current_table = session.get("current_user_table")
    if current_table:
        return redirect(url_for('dynamic_table_data', table_name=current_table))
    return "No table specified", 400

# ----------------------------------------------------------------------------------------------

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data, method='pbkdf2:sha256')
        new_user = User(username=form.username.data, password=hashed_password, age=form.age.data, weight=form.weight.data)
        db.session.add(new_user)
        db.session.commit()
        flash('Registration successful! Please login.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            return redirect(url_for('index_page'))
        else:
            flash('Login unsuccessful. Please check your username and password.', 'danger')
    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index_page'))

@app.route('/home')
def home():
    return redirect(url_for('index_page'))

@app.route("/")
def index_page():
    if current_user.is_authenticated:
        username = current_user.username
    else:
        username = None
    return render_template("index.html", user=username)

@app.route('/workout_plan')
@login_required
def workout_plan():
    return redirect(url_for('workout_plan_page'))

@app.route('/workout_plan_page')
@login_required
def workout_plan_page():
    


    return render_template("workout.html")

@app.route('/table_layout', methods=['GET', 'POST'])
@login_required
def table_layout():
    if request.method == "POST":
        exrs = request.form.get("xcrs")
        planned_exrs = request.form.get("weekly")
        mesocycle = request.form.get("mesocycle")
        deload = request.form.get("deload")
        
        # Set value of mesocycles to 0 for easier work in future
        user = User.query.filter_by(username=current_user.username).first()
        if user and (user.mesocycles is None):
            user.mesocycles = 0
            db.session.commit() 

        try:
            per_week = int(request.form.get("weekly", 0))
            if per_week <= 0:
                raise ValueError("Weekly value must be greater than zero.")
        except (TypeError, ValueError) as e:
            return "Invalid input for 'weekly': " + str(e), 400

        num_rows = int(request.form["xcrs"])
        num_cols = 3

        table_data = []
        for i in range(num_rows):
            row_data = []
            starter = 0
            for j in range(num_cols):
                cell_value = ''  # <- This can be adjusted as needed
                row_data.append(cell_value)
            table_data.append(row_data)

        session["table_data"] = table_data
        session["weekly"] = per_week
        session["starter"] = starter
        session['excercise'] = exrs

        # Create tables below:
        
        username = current_user.username
        
        # Before we let our user create new table we need to restrict his access to DB so no SQL injections are possible
        if not re.match(r'^\w+$', username) :
            return jsonify({"error": "Invalid username"})       

        # Find names of all tables
        inspect_db_names = inspect(db.engine)
        tables = inspect_db_names.get_table_names()
        
        compare = [i for i in tables if username in i] # How many times there is username in table names

        return redirect("create_workout")
    return render_template("table_layout.html")

# Here is created mesocycle workout
@app.route("/create_workout", methods=["GET", "POST"])
@login_required
def create_workout():
    table_data = session.get("table_data", [])
    weekly = session.get("weekly", 0)
    starter = session.get("starter", 0)
    current_table = session.get("current_user_table")
    exercises_per_session = session.get("excercise")
        
    if request.method == "POST":
        submitted_data = {}

        for key, value in request.form.items():
            if key.startswith("table_"):
                parts = key.split('_')
                table_index = int(parts[1])
                row_index = int(parts[3])
                col_index = int(parts[5])

                if table_index not in submitted_data:
                    submitted_data[table_index] = {}
                if row_index not in submitted_data[table_index]:
                    submitted_data[table_index][row_index] = {}

                submitted_data[table_index][row_index][col_index] = value

        # Create as many tables as I have sessions per week
        def create_tables_dynamically():
            user = User.query.filter_by(username=current_user.username).first()
            if user and (user.mesocycles is None):
                user.mesocycles = 0
                db.session.commit()
            elif user.mesocycles >= 1: 
                user.mesocycles += 1
                db.session.commit()
            elif user and (user.mesocycles == 0 or user.mesocycles < 1):
                user.mesocycles = 1
                db.session.commit()
        
            for one_session in range(int(weekly)):  
                table_name = f"{current_user.username}_M{user.mesocycles}_{one_session}"
                sql = text(f"""
                CREATE TABLE IF NOT EXISTS {table_name} (
                    id INTEGER PRIMARY KEY,
                    exercise TEXT NOT NULL,
                    sets INTEGER,
                    pauses FLOAT,
                    first_set INTEGER,
                    weight_first_set FLOAT,
                    rpe_first_set FLOAT,
                    second_set INTEGER,
                    weight_second_set FLOAT,
                    rpe_second_set FLOAT,
                    third_set INTEGER, 
                    weight_third_set FLOAT,
                    rpe_third_set FLOAT,
                    notes TEXT
                )
                """)

                try:
                    connection = db.session.connection()
                    connection.execute(sql)
                    print(f"Table '{table_name}' created successfully!")        
                except Exception as e:
                    print(f"Error creating table '{table_name}': {e}")

                # Save exercises to corresponding tables
                # Chosen exercises, sets and reps
                for exercise in range(int(exercises_per_session)):
                    
                    current_ecercise = submitted_data[one_session][exercise][0]
                    current_sets = submitted_data[one_session][exercise][1]
                    current_pause = submitted_data[one_session][exercise][2]
                    
                    try:
                        data = text(f'''
                        INSERT INTO {table_name} (exercise, sets, pauses)
                        VALUES ('{current_ecercise}', {current_sets}, {current_pause})
                        ''')
                        connection = db.session.connection()
                        connection.execute(data)
                        connection.commit()
                        print(f"Saved data into '{table_name}'")
                    except IntegrityError as e:
                        print(f"IntegrityError: {e}")
                    except Exception as e:
                        print(f"Something went wrong and I didn't save your stuff: {e}")
                print(f"length of submitted data = {len(submitted_data)}\nlength of weekly = {weekly}")
        
        create_tables_dynamically()
        return redirect(url_for("workout_plan_page"))

    return render_template("create_workout.html", table_data=table_data, weekly=weekly, st=starter, enumerate=enumerate)

@app.route('/training_session_redirect')
def training_session_redirect():
    return redirect(url_for('training_session'))

@app.route('/training_session', methods=["GET", "POST"])
@login_required
def training_session():
    return render_template('training_session.html')

# Delete in a moment if I don't forget
@login_required
@app.route('/execute_workout_plan_exercises')
def execute_workout_plan_exercises(): 
    return render_template("<h1>Just test if process will pass<h1>")

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
