from flask import Flask, render_template, request, redirect, url_for, flash, session
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Function to connect to the SQLite database
def get_db_connection():
    conn = sqlite3.connect('users.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def home():
    return render_template('index.html')

# Registration route
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']  # Capture the email input
        password = request.form['password']  # Capture the password input
        hashed_password = generate_password_hash(password)

        conn = get_db_connection()
        cursor = conn.cursor()

        # Insert user details including email
        try:
            cursor.execute("INSERT INTO users (username, password, email) VALUES (?, ?, ?)", 
                           (username, hashed_password, email))
            conn.commit()
            flash('User registered successfully!')
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            flash('Username or email already exists. Please try again.')
        finally:
            conn.close()

    return render_template('register.html')


# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
        user = cursor.fetchone()
        conn.close()

        if user and check_password_hash(user['password'], password):
            session['username'] = username
            flash('Login successful!')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid credentials, please try again.')

    return render_template('login.html')

# Dashboard route
@app.route('/dashboard')
def dashboard():
    if 'username' in session:
        return render_template('dashboard.html', username=session['username'])
    else:
        flash('Please login first!')
        return redirect(url_for('login'))
    

# Profile route
@app.route('/profile', methods=['GET', 'POST'])
def profile():
    if 'username' in session:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username = ?", (session['username'],))
        user = cursor.fetchone()
        conn.close()

        if request.method == 'POST':
            if 'update_password' in request.form:
                new_password = request.form['new_password']
                hashed_password = generate_password_hash(new_password)

                conn = get_db_connection()
                cursor = conn.cursor()
                cursor.execute("UPDATE users SET password = ? WHERE username = ?", (hashed_password, session['username']))
                conn.commit()
                conn.close()

                flash('Password updated successfully!')
                return redirect(url_for('profile'))

            elif 'update_email' in request.form:
                new_email = request.form['new_email']

                # Validate the new email if necessary (e.g., check for existing email)
                conn = get_db_connection()
                cursor = conn.cursor()
                cursor.execute("UPDATE users SET email = ? WHERE username = ?", (new_email, session['username']))
                conn.commit()
                conn.close()

                flash('Email updated successfully!')
                return redirect(url_for('profile'))

        return render_template('profile.html', user=user)
    else:
        flash('Please login first!')
        return redirect(url_for('login'))


# Add Plans route
@app.route('/add_plans', methods=['GET', 'POST'])
def add_plans():
    if request.method == 'POST':
        plan_name = request.form['plan_name']
        plan_duration = request.form['plan_duration']
        plan_price = request.form['plan_price']

        # Add the new plan to the database here
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO plans (name, duration, price) VALUES (?, ?, ?)", 
                       (plan_name, plan_duration, plan_price))
        conn.commit()
        conn.close()

        flash('Plan added successfully!')
        return redirect(url_for('add_plans'))

    # Fetch existing plans to display
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM plans")
    plans = cursor.fetchall()
    conn.close()

    return render_template('add_plans.html', plans=plans)

#Remove Plan
@app.route('/delete_plan', methods=['POST'])
def delete_plan():
    if 'username' in session:
        plan_id = request.form.get('plan_id')
        
        if plan_id:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM plans WHERE id = ?", (plan_id,))
            conn.commit()
            conn.close()
            
            flash('Plan deleted successfully!')
        else:
            flash('No plan ID provided!')

        return redirect(url_for('add_plans'))
    else:
        flash('Please login first!')
        return redirect(url_for('login'))



@app.route('/register_member', methods=['GET', 'POST'])
def register_member():
    if 'username' in session:
        if request.method == 'POST':
            try:
                name = request.form['name']
                surname = request.form['surname']
                age = request.form['age']
                address = request.form['address']
                mobile = request.form['mobile']
                email = request.form['email']
                plan_id = int(request.form['plan_id'])  # Updated to match the form
                payment_method = request.form['payment_method']

                conn = get_db_connection()
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO members (name, surname, age, address, mobile, email, plan_id, payment_method) 
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """, (name, surname, age, address, mobile, email, plan_id, payment_method))
                conn.commit()
                conn.close()

                flash('Member registered successfully!')
            except Exception as e:
                flash(f'Error occurred: {e}')
                return redirect(url_for('register_member'))

        # Fetch available plans
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, name, price FROM plans")  # Ensure columns are correct
        plans = cursor.fetchall()
        conn.close()

        return render_template('register_member.html', plans=plans)
    else:
        flash('Please login first!')
        return redirect(url_for('login'))




# View Members route
@app.route('/view_members')
def view_members():
    if 'username' in session:
        conn = get_db_connection()
        cursor = conn.cursor()
        # Adjust the SQL query to fetch specific columns, including plan name and status
        cursor.execute('''
    SELECT m.id, m.name, m.surname, m.age, m.address, m.mobile, m.email, p.name AS plan_name, m.payment_method, m.registration_date
    FROM members m
    LEFT JOIN plans p ON m.plan_id = p.id
''')

        members = cursor.fetchall()
        conn.close()

        return render_template('view_members.html', members=members)
    else:
        flash('Please login first!')
        return redirect(url_for('login'))

#Remove Member
@app.route('/remove_member', methods=['POST'])
def remove_member():
    if 'username' in session:
        member_id = request.form['member_id']
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM members WHERE id = ?", (member_id,))
        conn.commit()
        conn.close()
        flash('Member removed successfully!')
        return redirect(url_for('view_members'))
    else:
        flash('Please login first!')
        return redirect(url_for('login'))


# Route for adding coaches
@app.route('/add_coaches', methods=['GET', 'POST'])
def add_coaches():
    if 'username' in session:
        if request.method == 'POST':
            name = request.form['name']
            age = request.form['age']
            experience = request.form['experience']
            email = request.form['email']
            mobile = request.form['mobile']

            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("INSERT INTO coaches (name, age, experience, email, mobile) VALUES (?, ?, ?, ?, ?)",
                           (name, age, experience, email, mobile))
            conn.commit()
            conn.close()

            flash('Coach added successfully!')
            return redirect(url_for('add_coaches'))

        return render_template('add_coaches.html')
    else:
        flash('Please login first!')
        return redirect(url_for('login'))

# View Coaches route
@app.route('/view_coaches')
def view_coaches():
    if 'username' in session:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM coaches")
        coaches = cursor.fetchall()
        conn.close()

        return render_template('view_coaches.html', coaches=coaches)
    else:
        flash('Please login first!')
        return redirect(url_for('login'))
    
#Remove Coach
@app.route('/remove_coach', methods=['POST'])
def remove_coach():
    coach_id = request.form.get('coach_id')  # Get the coach ID from the form
    if coach_id:
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            # Delete the coach from the database
            cursor.execute("DELETE FROM coaches WHERE id = ?", (coach_id,))
            conn.commit()
            conn.close()
            flash('Coach removed successfully!', 'success')  # Flash success message
        except Exception as e:
            flash(f'Error removing coach: {e}', 'error')  # Flash error message
    else:
        flash('No coach ID provided!', 'error')  # Flash error if no ID is provided

    return redirect(url_for('view_coaches'))  # Redirect to the view coaches page
    

# Add Equipments route
@app.route('/add_equipments', methods=['GET', 'POST'])
def add_equipments():
    if 'username' in session:
        if request.method == 'POST':
            name = request.form['name']
            quantity = request.form['quantity']

            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("INSERT INTO equipments (name, quantity) VALUES (?, ?)", (name, quantity))
            conn.commit()
            conn.close()

            flash('Equipment added successfully!')
            return redirect(url_for('add_equipments'))

        return render_template('add_equipments.html')
    else:
        flash('Please login first!')
        return redirect(url_for('login'))

# View Equipments route
@app.route('/view_equipments')
def view_equipments():
    if 'username' in session:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM equipments")
        equipments = cursor.fetchall()
        conn.close()

        return render_template('view_equipments.html', equipments=equipments)
    else:
        flash('Please login first!')
        return redirect(url_for('login'))
    
#Remove Equipments
@app.route('/remove_equipment', methods=['POST'])
def remove_equipment():
    equipment_id = request.form.get('equipment_id')
    
    if equipment_id:
        conn = get_db_connection()
        try:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM equipments WHERE id = ?', (equipment_id,))
            conn.commit()
            flash('Equipment removed successfully!', 'success')
        except Exception as e:
            flash('Error removing equipment: {}'.format(e), 'error')
        finally:
            conn.close()
    else:
        flash('Invalid equipment ID!', 'error')

    return redirect(url_for('view_equipments'))

# Sales Report route
@app.route('/sales_report', methods=['GET', 'POST'])
def sales_report():
    if 'username' in session:
        total_registrations = 0  # Placeholder value
        total_earnings = 0  # Placeholder value
        registrations = []

        if request.method == 'POST':
            start_date = request.form['start_date']
            end_date = request.form['end_date']

            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("""
                SELECT m.name, m.email, p.name, m.payment_method, m.registration_date
                FROM members m
                JOIN plans p ON m.plan_id = p.id
                WHERE m.registration_date BETWEEN ? AND ?
            """, (start_date, end_date))
            registrations = cursor.fetchall()

            cursor.execute("""
                SELECT COUNT(*) AS total_registrations, SUM(p.price) AS total_earnings
                FROM members m
                JOIN plans p ON m.plan_id = p.id
                WHERE m.registration_date BETWEEN ? AND ?
            """, (start_date, end_date))
            result = cursor.fetchone()
            total_registrations = result['total_registrations']
            total_earnings = result['total_earnings']
            conn.close()

        return render_template('sales_report.html', total_registrations=total_registrations,
                               total_earnings=total_earnings, registrations=registrations)
    else:
        flash('Please login first!')
        return redirect(url_for('login'))

# Logout route
@app.route('/logout')
def logout():
    session.pop('username', None)
    flash('You have been logged out!')
    return redirect(url_for('login'))











if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

