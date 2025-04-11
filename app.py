import json
import os
from flask import Flask, render_template, request, redirect, url_for, jsonify
from werkzeug.utils import secure_filename
from datetime import datetime
from flask import flash

app = Flask(__name__)

# Configurations
UPLOAD_FOLDER = 'static/uploads'
JSON_FILE = 'assignments.json'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure the upload directory exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Ensure the JSON file exists
if not os.path.exists(JSON_FILE):
    with open(JSON_FILE, 'w') as file:
        json.dump({"assignments": []}, file)

# Helper function to read JSON
def read_assignments():
    with open(JSON_FILE, 'r') as file:
        return json.load(file)
# Function to read submissions from the JSON file
def read_submissions():
    with open('submissions.json', 'r') as file:
        data = json.load(file)
    return data


# Function to save submissions in a JSON file
def save_submission(submission_data):
    submissions = read_submissions()
    submissions.append(submission_data)
    with open('submissions.json', 'w') as file:
        json.dump(submissions, file, indent=4)

# Helper function to write JSON
def write_assignments(data):
    with open(JSON_FILE, 'w') as file:
        json.dump(data, file, indent=4)

@app.route('/upload_assignment', methods=['POST'])
def upload_assignment():
    if request.method == 'POST':
        # Validate that files are provided
        assignment_file = request.files.get('assignmentFile')
        solution_file = request.files.get('solutionFile')

        if not assignment_file or assignment_file.filename == '':
            return jsonify({"error": "Assignment file is missing"}), 400
        if not solution_file or solution_file.filename == '':
            return jsonify({"error": "Solution file is missing"}), 400

        # Save files securely
        assignment_filename = secure_filename(assignment_file.filename)
        solution_filename = secure_filename(solution_file.filename)

        assignment_file.save(os.path.join(app.config['UPLOAD_FOLDER'], assignment_filename))
        solution_file.save(os.path.join(app.config['UPLOAD_FOLDER'], solution_filename))

        # Process other form data
        assignment_name = request.form['assignmentName']
        assignment_description = request.form['assignmentDescription']
        due_date = request.form['dueDate']

        # Load existing assignments and add the new one
        assignments_data = read_assignments()
        new_id = len(assignments_data['assignments']) + 1

        new_assignment = {
            "id": new_id,
            "name": assignment_name,
            "description": assignment_description,
            "due_date": due_date,
            "assignment_file": os.path.join('uploads', assignment_filename),
            "solution_file": os.path.join('uploads', solution_filename),
            "timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }

        assignments_data['assignments'].append(new_assignment)
        write_assignments(assignments_data)

        return redirect(url_for('view_ctai'))  # Redirect to a list page after submission

@app.route('/assignments', methods=['GET'])
def get_assignments():
    assignments_data = read_assignments()
    return jsonify(assignments_data)

@app.route('/')
def index():
    return render_template('login.html')  # Renders the login page


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        role = request.form.get('role')  # Get the role (student or teacher)

        # Example validation logic
        if role == "student":
            if email == "student@vit.edu" and password == "student123":
                return redirect(url_for('student'))
            else:
                return "Invalid student credentials", 401

        elif role == "teacher":
            if email == "teacher@vit.edu" and password == "teacher123":
                return redirect(url_for('teacher_dashboard'))
            else:
                return "Invalid teacher credentials", 401

        else:
            return "Invalid role selected", 400

    # Render the login page on GET
    return render_template('login.html')



@app.route('/teacher_dashboard')
def teacher_dashboard():
    return render_template('teacher_dashboard.html')  # Renders the dashboard page


# Path to the JSON file where submissions are stored
SUBMISSIONS_FILE = 'submissions.json'


# Function to load or initialize the JSON file
def load_submissions():
    if os.path.exists(SUBMISSIONS_FILE):
        with open(SUBMISSIONS_FILE, 'r') as file:
            return json.load(file)
    return []


# Function to save data to the JSON file
def save_submissions(submissions):
    with open(SUBMISSIONS_FILE, 'w') as file:
        json.dump(submissions, file, indent=4)

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    assignments_data = read_assignments()
    
    if request.method == 'POST':
        assignment_id = int(request.form['assignment_id'])
        # Hardcode values for name and rollno
        student_name = 'Harshada'
        rollno = '45'
        file = request.files['file']
        
        if file:
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            
            # Prepare submission data
            submission_data = {
                'id': assignment_id,
                'assignment_name': request.form['assignment_name'],
                'name': student_name,  # Hardcoded name
                'rollno': rollno,      # Hardcoded roll number
                'file_path': file_path,
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
            
            # Save the submission
            save_submission(submission_data)
            return redirect(url_for('assign_submitted_msg'))  # Redirect to dashboard after submission

    return render_template('dashboard.html', assignments=assignments_data['assignments'])


# @app.route('/assessment', methods=['GET', 'POST'])
# def assessment():
#     if request.method == 'POST':
#         # Handle assessment submission here
#         answers = request.form.to_dict()  # Example to collect all form data
#         # Process answers, calculate scores, etc.
#         return render_template('assessment.html', success="Assessment submitted successfully")
#     return render_template('assessment.html')  # Renders the assessment page

@app.route('/create')
def create():
    return render_template('create.html')

@app.route('/assign_submitted_msg')
def assign_submitted_msg():
    return render_template('assign_submitted.html')

@app.route('/list_ai')
def list_ai():
    try:
        # Open the submissions.json file and load the data
        with open('submissions.json') as f:
            submissions_data = json.load(f)

        # Debug: print the data to check its structure
        print(f"Type of submissions_data: {type(submissions_data)}")
        print(f"Content of submissions_data: {submissions_data}")

        # Ensure that submissions_data is a list (not a dictionary)
        if not isinstance(submissions_data, list):
            print("Error: The data is not in the expected format (expected a list).")
            return "Error: The data is not in the expected format (expected a list).", 400

        # Render the template with all submissions data
        return render_template('listAI.html', submissions=submissions_data)

    except Exception as e:
        print(f"Error: {e}")
        return f"An error occurred: {e}", 500


@app.route('/list_ml')
def list_ml():
    return render_template('listML.html')

@app.route('/list_os')
def list_os():
    return render_template('listOS.html')

@app.route('/student', methods=['GET'])
def student():
    return render_template('student.html')


@app.route('/view_ctai')
def view_ctai():
    assignments_data = read_assignments()
    return render_template('viewCTAI.html', assignments=assignments_data['assignments'])
    

@app.route('/view_ctml')
def view_ctml():
    return render_template('ViewCTML.html')

@app.route('/view_ctos')
def view_ctos():
    return render_template('viewCTOS.html')

@app.route('/view_ctsi')
def view_ctsi():
    return render_template('viewCTSI.html')


# Route to handle assignment submission
@app.route('/submit_assignment', methods=['POST'])
def submit_assignment():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['file']
    name = "45"
    roll_no = "Harshada"
    assignment_name = request.form.get('assignment_name')

    if file.filename == '':
        return jsonify({"error": "No file selected"}), 400

    # Save the file
    filename = file.filename
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(file_path)

    # Create submission record
    submission = {
        "name": "Harshada",
        "roll_no": 45,
        "submission_timestamp": datetime.now().isoformat(),
        "assignment_name": assignment_name,
        "file_path": file_path
    }

    # Load, update, and save the JSON file
    submissions = load_submissions()
    submissions.append(submission)
    save_submissions(submissions)

    return jsonify({"message": "File uploaded successfully", "submission": submission}), 200



#for dashboard assignment view

@app.route('/assignments.json')
def assignments():
    with open('assignments.json') as f:
        assignments_data = json.load(f)
    return jsonify(assignments_data)


# result
@app.route('/result')
def result():
    submission_id = request.args.get('submission_id')
    # Fetch result data using submission_id
    result_data = get_result_data(submission_id)  # Example function
    return render_template('result.html', result=result_data)

if __name__ == '__main__':
    app.run(debug=True)
