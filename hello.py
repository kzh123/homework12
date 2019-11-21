"""
testing
"""

from flask import Flask, render_template
import sqlite3

app = Flask(__name__)


@app.route('/Hello')
def hello():
    return "This is Flask!"


@app.route('/GoodBye')
def see_ya():
    return "See ya!"


@app.route('/sample_template')
def template_demo():
    return render_template('parameters.html',
                           my_header='My Stevens Repository',
                           my_param='My custom parameter')


@app.route('/students')
def student_course():
    dbpath = './810_startup.db'
    try:
        db = sqlite3.connect(dbpath)
    except sqlite3.OperationalError:
        return f"Error: Unable to open database at {dbpath}"
    else:

        query = """select InstructorCWID, Name, Dept, Course, count(g.StudentCWID) as StudentsNumber
from instructors i
    join grades g
        on i.CWID = g.InstructorCWID
group by g.Course, g.InstructorCWID"""

        data = [{'cwid': InstructorCWID, 'name': Name, 'dept': Dept, 'course': Course, 'student_number': StudentsNumber}
                for InstructorCWID, Name, Dept, Course, StudentsNumber in db.execute(query)]

        db.close()

        return render_template(
            'student_course.html',
            title='Stevens Repository',
            table_title="Number of completed courses by Student",
            instructors=data
        )


app.run(debug=True)
