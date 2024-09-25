from flask import Flask, render_template, redirect, request
import requests
from difflib import HtmlDiff
from pathlib import Path
import os
import sqlite3
import zipfile
import glob
import logging


database = sqlite3.connect("database.sqlite3")

# database.execute("DROP TABLE graded_submissions;") # for easy table death
database.execute("CREATE TABLE IF NOT EXISTS graded_submissions (name TEXT);")

def submission_filename_to_student_id(filename) -> str:
    filename = str(filename)
    # _lastfirst, _unknown, student_id, _filename = filename.split(sep="_", maxsplit=3)
    student_id = filename
    return student_id

def generate_file_diff_html(submission_path: Path, original_code_root: Path) -> str:
    html_differ = HtmlDiff()

    # Find the app.py file to figure out where the "root" of the submission is
    app_py_path = list(glob.glob(submission_path + "**/app.py", root_dir="submissionFileFolder/"))
    print(app_py_path)
    if len(app_py_path) != 1:
        logging.warning(f"Unable to find a single app.py: {app_py_path}")
        return "Invalid submission"
    else:
        root_path = "submissionFileFolder/" + submission_path

    file_diffs = []
    for file in glob.glob(root_path + "**/*"):
        # Skip results which are directories or non-text files
        # file = root_path + "/" + file
        file = Path(file)

        if not file.is_file():
            continue

        if file.suffix in {".sqlite3", ".jpg", ".css", ".pyc", ".sql", ".md"}:
            continue

        print(file)

        try:
            relative_path = file.relative_to(root_path)
        except ValueError:
            # If the file is not inside the root folder, ignore it
            continue

        # Find the corrosponding file in the original code
        original_file = Path(original_code_root, relative_path)
        print(original_file)

        # Read both files, if they exist
        if original_file.is_file():
            original_lines = original_file.read_text().splitlines()
        else: 
            original_lines = []
        updated_lines = file.read_text().splitlines()

        # Diff both files
        html_diff = html_differ.make_table(original_lines, updated_lines, fromdesc=relative_path, todesc=submission_path, numlines=2, context=True)
        if "No Differences Found" not in html_diff:
            file_diffs.append(html_diff)

    for file in glob.glob("**/*", root_dir=root_path):
        # Skip results which are directories or non-text files
        file = root_path + "/" + file
        file = Path(file)
        
        if not file.is_file():
            continue

        if file.suffix in {".sqlite3", ".jpg", ".css", ".pyc", ".sql", ".md"}:
            continue

        print(file)

        try:
            relative_path = file.relative_to(root_path)
        except ValueError:
            # If the file is not inside the root folder, ignore it
            continue

        # Find the corrosponding file in the original code
        original_file = Path(original_code_root, relative_path)
        print(original_file)

        # Read both files, if they exist
        if original_file.is_file():
            original_lines = original_file.read_text().splitlines()
        else: 
            original_lines = []
        updated_lines = file.read_text().splitlines()

        # Diff both files
        html_diff = html_differ.make_table(original_lines, updated_lines, fromdesc=relative_path, todesc=submission_path, numlines=2, context=True)
        if "No Differences Found" not in html_diff:
            file_diffs.append(html_diff)
            # file_diffs.append("<br>")
    
    # Return all of the file diffs joined together

    html = """
    <style type="text/css">
        table.diff {font-family:Courier; border:medium;}
        .diff_header {background-color:#e0e0e0}
        td.diff_header {text-align:right}
        .diff_next {background-color:#c0c0c0}
        .diff_add {background-color:#aaffaa}
        .diff_chg {background-color:#ffff77}
        .diff_sub {background-color:#ffaaaa}
    </style>
    """ + "\n".join(file_diffs)
    # html = file_diffs

    return html

submission_path_map = {}
path_map_max = 0
path_map_index_key = {}
path_map_iter = 0

pathList = []
subFilePath = Path()
for filename in os.scandir(os.path.join(subFilePath.resolve(), 'insertMainZipHere')):
    # print(filename.name)
    pathList.append(filename.name)

mainZip = glob.glob("insertMainZipHere/*.zip")
# print(mainZip)
if len(pathList) == 1:
    with zipfile.ZipFile(mainZip[0], 'r') as zip_ref:
        zip_ref.extractall("submissionFileFolder")

pathList = []
subFilePath = Path()
for filename in os.scandir(os.path.join(subFilePath.resolve(), 'submissionFileFolder')):
    # print(filename.name)
    pathList.append(filename.name)
# print(pathList)
pathListIndex = 0
pathListSize = len(pathList)

all_zip_files = glob.glob("*.zip", recursive=False, root_dir="submissionFileFolder/")
for submission in all_zip_files:
    with zipfile.ZipFile("submissionFileFolder/" + submission, 'r') as zip_ref:
        fileRoute = submission[:-4]
        zip_ref.extractall("submissionFileFolder/")
        idNum = submission_filename_to_student_id(submission)
        submission_path_map.update({path_map_max: fileRoute}) #idNum
    # path_map_index_key.update({path_map_iter: idNum})
    path_map_max += 1
print(submission_path_map)

database.row_factory = lambda cursor, row: row[0]
cursor = database.cursor()
cursor.execute("SELECT name from graded_submissions;")
gradedList = cursor.fetchall()
# print(gradedList)
database.commit()
database.close()

# initial_run_check = True

source_file = 'original_code'
submission_file = submission_path_map[path_map_iter] #path_map_index_key[]
# currentSubDirectory = ''

# for i in range(0, pathListSize): #Function for skip to next ungraded student, comment out to disable
#     if pathList[i] not in gradedList:
#         submission_file = pathList[i]
#         pathListIndex = i
#         break
        #DEPRECATED, NEED TO FIX

# submission_file = 'testFileFolder/' + current_file

app = Flask(__name__)

@app.route('/')
# def hello():
#     return 'Hello, World!'
def index():
    global source_file
    global submission_file
    global gradedList
    # global currentSubDirectory
    # print(gradedList)

    # if submission_file
    # subFileRoute = 'submissionFileFolder/' + submission_file

    # if submission_file[-4:] == ".zip":
    #     with zipfile.ZipFile(subFileRoute, 'r') as zip_ref:
    #         zip_ref.extractall(subFileRoute[:-4])
    # currentSubDirectory = submission_file[:-4]


    # file_1 = open(source_file, 'r')
    # file_2 = open('submissionFileFolder/' + submission_file, 'r')
    
    # differ = HtmlDiff() 
    diffTable = generate_file_diff_html(submission_path_map[path_map_iter], source_file)
    # diffTable = differ.make_table(file_1, file_2, fromdesc='Provided Assignment Key', todesc=('Student Submission: ' + submission_file), context=True, numlines=2)

    # file_1.close() 
    # file_2.close() 

    # if (all(e in gradedList for e in pathList)):
        # return render_template('index.html', diff=diffTable, graded_verifier='All submissions graded! unless something went horribly wrong')
    # else:
    return render_template('index.html', diff=diffTable)


@app.route('/diffSubmissionPrev', methods=['POST'])
def prev():
    global submission_file
    global submission_path_map
    global path_map_iter
    global path_map_index_key
    # global pathListSize
    if path_map_iter > 0:
        path_map_iter -= 1
        submission_file = submission_path_map[path_map_iter]

    return redirect('/')

@app.route('/diffSubmissionNext', methods=['POST'])
def next():
    global submission_file
    global submission_path_map
    global path_map_iter
    global path_map_index_key

    if path_map_iter < len(submission_path_map)-1:
        path_map_iter += 1
        submission_file = submission_path_map[path_map_iter]

    return redirect('/')

@app.route('/postGrade100', methods=['POST'])
def grade100():
    global submission_file
    global gradedList
    database = sqlite3.connect("database.sqlite3")
    
    database.execute(f"INSERT INTO graded_submissions (name) VALUES ('{submission_file}');")
    gradedList.append(submission_file)

    database.commit()
    database.close()

    grade_dict = {
    'problem_key' : 123456789, #default
    'username' : 'poiu1234', #default, needs to read and scrape from submission_file name
    'grade' : 100, #hardcode
    'comments' : "", #hardcode
    }
    print("grade 100!")

    r = requests.post('https://staging.csci3403.com/api/grade/', data=grade_dict)
    
    # print (
    #     r,
    #     r.text,
    #     r.status_code,
    #     r.headers['content-type'],
    # )

    next()
    return redirect('/')

@app.route('/postGradePartial', methods=['POST'])
def gradePartial():
    global submission_file
    global gradedList
    database = sqlite3.connect("database.sqlite3")
    
    database.execute(f"INSERT INTO graded_submissions (name) VALUES ('{submission_file}');")
    gradedList.append(submission_file)

    database.commit()
    database.close()

    grade_dict = {
    'problem_key' : 123456789, #default
    'username' : 'poiu1234', #default
    'grade' : request.form['gradeValue'], #hardcode
    'comments' : request.form['feedbackValue'], #hardcode
    }
    print("partial grade", request.form['gradeValue'])
    print(request.form['feedbackValue'])

    r = requests.post('https://staging.csci3403.com/api/grade/', data=grade_dict)
    
    # print (
    #     r,
    #     r.text,
    #     r.status_code,
    #     r.headers['content-type'],
    # )

    next()
    return redirect('/')

app.run(debug=True)