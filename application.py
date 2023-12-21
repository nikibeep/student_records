from flask import Flask, render_template, request
import mysql.connector

application = Flask(__name__)

# MySQL configuration
db_config = {
    'host': 'studentdb.cbljczdcazj2.us-east-1.rds.amazonaws.com',
    'user': 'admin',
    'password': '12345678',
    'database': 'Student'
}

try:
    # Establish connection to MySQL
    connection = mysql.connector.connect(**db_config)
    if connection.is_connected():
        print("Connected to MySQL database!")
    else:
        print("MySQL connection failed!")
except mysql.connector.Error as e:
    print("Error connecting to MySQL:", e)
    
connection = mysql.connector.connect(**db_config)

cursor = connection.cursor()

# Create table if not exists
try:
    cursor = connection.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Student_details (
            Student_Name VARCHAR(255),
            Date_of_Record DATE,
            Research_Papers INT,
            Subjects INT,
            Passed INT,
            Failed INT,
            Average INT
        )
    ''')
except mysql.connector.Error as e:
    print("Error creating table:", e)


# Route to display the form for entering data
@application.route('/enter_data', methods=['GET'])
def show_data_input_form():
    return render_template('student_data_input.html')

# Route to handle form submission
@application.route('/submit_form', methods=['POST'])
def submit_form():
    if request.method == 'POST':
        student_name = request.form.get('student_name')
        date_of_record = request.form.get('date_of_record')
        research_papers = request.form.get('research_papers')
        subjects = request.form.get('subjects')
        passed = request.form.get('passed')
        failed = request.form.get('failed')
        average = request.form.get('average')

        try:
            query = """INSERT INTO Student_details (Student_Name, Date_of_Record, Research_Papers, Subjects,
                       Passed, Failed, Average)
                       VALUES (%s, %s, %s, %s, %s, %s, %s)"""
            values = (student_name, date_of_record, research_papers, subjects, passed, failed, average)

            cursor.execute(query, values)
            connection.commit()

            return 'Form submitted successfully'
        except mysql.connector.Error as e:
            print("Error:", e)
            return 'Failed to submit form'

# Route to display student records
@application.route('/Students', methods=['GET'])
def students():
    try:
        query = "SELECT Student_Name, Research_Papers FROM Student_details ORDER BY Research_Papers ASC"
        cursor.execute(query)
        data = cursor.fetchall()
        return render_template('Students.html', data=data)
    except mysql.connector.Error as e:
        print("Error:", e)
        return 'Failed to fetch data'

if __name__ == '__main__':
    application.run(debug=True, host='127.0.0.1', port=5000)