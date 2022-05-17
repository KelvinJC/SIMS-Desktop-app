
import datetime
import sqlite3

class Database:
    def __init__(self, db):
        # Create a connection to database file
        self.conn = sqlite3.connect(db, detect_types=sqlite3.PARSE_DECLTYPES |
                                                        sqlite3.PARSE_COLNAMES) # detect_types keyword arg is to ensure the date columns are parsed in as dates
        # Create cursor object
        self.cur = self.conn.cursor()
        self.cur.execute("""
                CREATE TABLE IF NOT EXISTS session (
                        session_id INTEGER NOT NULL PRIMARY KEY,
                        session_name TEXT NOT NULL,
                        resumption_date TEXT NOT NULL,
                        closing_date TEXT NOT NULL
                        );"""),
        self.cur.execute("""
                CREATE TABLE IF NOT EXISTS term (
                        term_id INTEGER NOT NULL PRIMARY KEY,
                        session_id INTEGER NOT NULL,
                        term_name TEXT NOT NULL,
                        resumption_date TEXT NOT NULL,
                        closing_date TEXT NOT NULL,
                        FOREIGN KEY (session_id) REFERENCES session (session_id)
                        );"""),
        self.cur.execute("""
                CREATE TABLE IF NOT EXISTS break (
                        break_id INTEGER NOT NULL PRIMARY KEY,
                        term_id INTEGER NOT NULL,
                        break_name INTEGER NOT NULL,
                        start_date TEXT NOT NULL,
                        end_date TEXT NOT NULL,
                        FOREIGN KEY (term_id) REFERENCES term (term_id)
                        );"""),
        self.cur.execute("""
                CREATE TABLE IF NOT EXISTS subject (
                        subject_id INTEGER NOT NULL PRIMARY KEY,
                        subject_name TEXT NOT NULL
                        );"""),
        self.cur.execute("""
                CREATE TABLE IF NOT EXISTS class (
                        class_id INTEGER NOT NULL PRIMARY KEY,
                        class_name TEXT NOT NULL UNIQUE
                        );"""),
        self.cur.execute("""
                CREATE TABLE IF NOT EXISTS student (
                        student_id INTEGER NOT NULL PRIMARY KEY,
                        student_first_name TEXT NOT NULL,
                        student_middle_name TEXT NULL,
                        student_last_name TEXT NOT NULL,
                        gender TEXT NOT NULL,
                        class_name TEXT NOT NULL,
                        FOREIGN KEY (class_name) REFERENCES class (class_name)
                        );"""),
        self.cur.execute("""
                CREATE TABLE IF NOT EXISTS enrolment (
                        enrolment_id INTEGER NOT NULL PRIMARY KEY,
                        subject_id INTEGER NOT NULL,
                        session_id INTEGER NOT NULL,
                        student_id INTEGER NOT NULL,
                        date TEXT NOT NULL,
                        FOREIGN KEY (subject_id) REFERENCES subject (subject_id),
                        FOREIGN KEY (session_id) REFERENCES session (session_id),
                        FOREIGN KEY (student_id) REFERENCES student (student_id)
                        );"""),
        self.cur.execute("""
                CREATE TABLE IF NOT EXISTS lesson_attendance (
                        id INTEGER NOT NULL PRIMARY KEY,
                        term_id INTEGER NOT NULL,
                        subject_id INTEGER NOT NULL,
                        student_id INTEGER NOT NULL,
                        date TEXT NOT NULL,
                        time TEXT NOT NULL,
                        FOREIGN KEY (subject_id) REFERENCES subject (subject_id),
                        FOREIGN KEY (student_id) REFERENCES student (student_id),
                        FOREIGN KEY (term_id) REFERENCES term (term_id)
                        );""")
        self.cur.execute("""
                CREATE TABLE IF NOT EXISTS school_attendance (
                        id INTEGER NOT NULL PRIMARY KEY,
                        term_id INTEGER NOT NULL,
                        student_id INTEGER NOT NULL,
                        date TEXT NOT NULL,
                        FOREIGN KEY (student_id) REFERENCES student (student_id),
                        FOREIGN KEY (term_id) REFERENCES term (term_id)
                        );"""),
        self.cur.execute("""
                CREATE TABLE IF NOT EXISTS assessment (
                        assessment_id INTEGER NOT NULL PRIMARY KEY,
                        subject_id INTEGER NOT NULL,
                        term_id INTEGER NOT NULL,
                        student_id INTEGER NOT NULL,
                        description TEXT NOT NULL,
                        score INTEGER NOT NULL,
                        max_score INTEGER NOT NULL,
                        date TEXT NOT NULL,
                        FOREIGN KEY (subject_id) REFERENCES subject (subject_id),
                        FOREIGN KEY (student_id) REFERENCES student (student_id)
                        );
                        """),
        self.cur.execute("""
                CREATE TABLE IF NOT EXISTS aggregate_score (
                        id INTEGER NOT NULL PRIMARY KEY,
                        term_id TEXT NOT NULL,
                        subject_id TEXT NOT NULL,
                        student_id TEXT NOT NULL,
                        score INTEGER NOT NULL,
                        FOREIGN KEY (student_id) REFERENCES student (student_id),
                        FOREIGN KEY (term_id) REFERENCES term (term_id),
                        FOREIGN KEY (subject_id) REFERENCES subject (subject_id)
                        );"""),
        self.conn.commit()

    # subject table
    def fetch_subject(self):
        self.cur.execute("SELECT * FROM subject")
        rows = self.cur.fetchall()
        return rows

    # Given a subject name, obtain the corresponding subject_id. For particular use in attendance.store_log_dict function.
    def fetch_subject_id(self, subject_name):
        self.cur.execute("SELECT subject_id FROM subject WHERE subject_name = ?",(subject_name,))
        rows = self.cur.fetchall()
        return rows

    def insert_subject(self, subject_name):
        self.cur.execute("INSERT INTO subject VALUES (NULL, ?)", (subject_name,))
        self.conn.commit()

    def update_subject(self, subject_id, subject_name):
        self.cur.execute("UPDATE subject SET subject_name = ? WHERE subject_id= ?", (subject_name, subject_id))
        self.conn.commit()

    # I suspect I will have to delete by subject_name rather than subject_id to be quicker. The current code suggests that the app will have to send fetch subject query to obtain subject name before knowing which subject to delete.
    def remove_subject(self, subject_id):
        self.cur.execute("DELETE FROM subject WHERE subject_id= ?", (subject_id,))
        self.conn.commit()

    # Class table
    def fetch_class(self):
        self.cur.execute("SELECT * FROM class")
        rows = self.cur.fetchall()
        return rows

    def insert_class(self, class_name):
        self.cur.execute("INSERT INTO class VALUES (NULL, ?)", (class_name,))
        self.conn.commit()

    def update_class(self, class_id, class_name):
        self.cur.execute("UPDATE class SET class_name = ? WHERE class_id = ?", (class_name, class_id))
        self.conn.commit()

    def remove_class(self, class_id):
        self.cur.execute("DELETE FROM class WHERE class_id = ?", (class_id,))
        self.conn.commit()

    # Student table
    def fetch_students_in_subject(self, subject_name):
        # To account for cases where single teacher teaches multiple subjects
        self.cur.execute("SELECT student.student_first_name, student.student_middle_name, student.student_last_name FROM student JOIN enrolment ON student.student_id = enrolment.student_id JOIN subject ON subject.subject_id = enrolment.subject_id WHERE subject.subject_name=?", (subject_name,))
        rows = self.cur.fetchall()
        return rows

    def fetch_students_in_class(self, class_name):
        self.cur.execute("SELECT student_id, student_first_name, student_middle_name, student_last_name FROM student WHERE class_name=?", (class_name,))
        rows = self.cur.fetchall()
        return rows

    def fetch_student(self):
        self.cur.execute("SELECT * FROM student")
        rows = self.cur.fetchall()
        return rows

    def fetch_student_count_by_gender(self, class_name, gender):
        self.cur.execute("SELECT COUNT(student.student_id) FROM student WHERE class_name = ? AND gender = ?", (class_name, gender,))
        rows = self.cur.fetchall()
        return rows

    def insert_student(self, student_first_name, student_middle_name, student_last_name, gender, class_name):
        self.cur.execute("INSERT INTO student VALUES (NULL, ?, ?, ?, ?, ?)", (student_first_name, student_middle_name, student_last_name, gender, class_name))
        self.conn.commit()

    def update_student(self, student_id, student_first_name, student_middle_name, student_last_name, gender, class_name):
        self.cur.execute("UPDATE student SET student_first_name = ?, student_last_name = ?, gender = ?, class_name = ? WHERE student_id= ?", (student_first_name, student_last_name, gender, class_name, student_id))
        self.conn.commit()

    def remove_student(self, student_id):
        self.cur.execute("DELETE FROM student WHERE student_id=?", (student_id,))
        self.conn.commit()

    def remove_students_in_selected_class(self, class_name): # May be temp measure until cascade is setup for when a class record is deleted
        self.cur.execute("DELETE FROM student WHERE class_name=?", (class_name,))
        self.conn.commit()

    # enrolment table
    def fetch_enrolment(self, subject_id):
        self.cur.execute("SELECT student.student_first_name, student.student_middle_name, student.student_last_name, student.class_name, subject.subject_name, enrolment.date FROM student JOIN enrolment ON enrolment.student_id = student.student_id JOIN subject ON enrolment.subject_id = subject.subject_id WHERE subject.subject_id =?", (subject_id,))
        rows = self.cur.fetchall()
        return rows

    def fetch_enrolments_grouped(self, subject_id):
        # This query collates all the student enrolments into a class enrolment
        self.cur.execute("SELECT COUNT(student.student_id), student.class_name, subject.subject_name FROM student JOIN enrolment ON enrolment.student_id = student.student_id JOIN subject ON enrolment.subject_id = subject.subject_id WHERE subject.subject_id = ? GROUP BY student.class_name", (subject_id,))
        rows = self.cur.fetchall()
        return rows

    def fetch_enrolments(self):
        # This query fetches individual student enrolments
        self.cur.execute("SELECT student.student_first_name, student.student_middle_name, student.student_last_name, student.class_name, subject.subject_name, enrolment.date FROM student JOIN enrolment ON enrolment.student_id = student.student_id JOIN subject ON enrolment.subject_id = subject.subject_id")
        rows = self.cur.fetchall()
        return rows

    def insert_enrolment(self, subject_id, session_id, student_id, date_time):
        self.cur.execute("INSERT INTO enrolment VALUES (NULL, ?, ?, ?, ?)", (subject_id, session_id, student_id, date_time))
        self.conn.commit()

    # Attendance table
            # Attendance is analytics, I'll come back to it along with the other analytics reports. I suspect there will be more than one fetch queries
    def fetch_lesson_attendance(self, subject_id, class_id):
        self.cur.execute("SELECT student.student_id, student.student_first_name, student.student_middle_name, student.student_last_name, class.class_name, COUNT(attendance_id) FROM class JOIN student ON class.class_id = student.class_id JOIN lesson_attendance ON lesson_attendance.student_id = student.student_id WHERE lesson_attendance.subject_id=? AND class.class_id =? GROUP BY student.student_id", (subject_id, class_id))
        rows = self.cur.fetchall()
        return rows

    def fetch_lesson_attendance_by_class(self, class_name): # AND WHERE date > [] insert resumption date of selected term
        self.cur.execute("SELECT student.student_id, student.student_first_name, student.student_middle_name, student.student_last_name, student.class_name, COUNT(lesson_attendance.id) FROM lesson_attendance JOIN student ON lesson_attendance.student_id = student.student_id WHERE student.class_name =? GROUP BY student.student_id", (class_name,))
        rows = self.cur.fetchall()
        return rows

    def fetch_all_lesson_attendance(self):
        self.cur.execute("SELECT * from lesson_attendance")
        rows = self.cur.fetchall()
        return rows

        # Leaving the subject_id and student_id entry as null with the assumption that secondary schools do not assign student or subject ids. Database set to generate it automatically
    def insert_lesson_attendance(self, term_id, subject_id, student_id, date, time):
        self.cur.execute("INSERT INTO lesson_attendance VALUES (NULL, ?, ?, ?, ?, ?)", (term_id, subject_id, student_id, date, time))
        self.conn.commit()

        # To prevent duplicate attendance records on same day
    def remove_duplicate_attendance(self): # Should this reference term?
        self.cur.execute("DELETE from lesson_attendance WHERE id NOT IN (SELECT MIN(id) FROM lesson_attendance GROUP BY date, subject_id , student_id)")
        self.conn.commit()

    def remove_attendance(self, attendance_id):
        self.cur.execute("DELETE FROM lesson_attendance WHERE id=?", (attendance_id,))
        self.conn.commit()

    # Assessment table (For order, these fetch functions are grouped by student, class & subject)
        # Student Analytics
    def fetch_assessment(self):
        # Pull records in a single assessment type for all students
        self.cur.execute("SELECT student.student_first_name, student.student_middle_name, student.student_last_name, student.class_name, subject.subject_name, assessment.description, assessment.score FROM student JOIN assessment ON student.student_id = assessment.student_id JOIN subject ON subject.subject_id = assessment.subject_id")
    def fetch_all_term_assessments(self, student_id, term_id):
        # Pull all the different assessment records in one term for a particular student
        self.cur.execute("SELECT student.student_first_name, student.student_middle_name, student.student_last_name, class.class_name, subject.subject_name, assessment.description, assessment.score, assessment.date FROM class JOIN student ON class.class_id = student.class_id JOIN assessment ON assessment.student_id = student.student_id JOIN enrolment ON enrolment.student_id = student.student_id JOIN subject on subject.subject_id = enrolment.subject_id WHERE student.student_id=? AND assessment.term_id = ?", (student_id, term_id))
        rows = self.cur.fetchall()
        return rows

    # TBD: Should add fetch_all_assessments which pulls all a students records in all terms

    def fetch_all_term_assessments_all_students(self, term_id): # Class An as well
        # Pull all the different assessment records on each student
        self.cur.execute("SELECT student.student_id, student.student_first_name, student.student_middle_name, student.student_last_name, subject.subject_name, assessment.description, assessment.score, assessment.date FROM assessment JOIN student ON assessment.student_id = student.student_id JOIN enrolment ON enrolment.student_id = student.student_id JOIN subject on subject.subject_id = enrolment.subject_id WHERE assessment.term_id = ? GROUP BY student.student_id", (term_id))
        rows = self.cur.fetchall()
        return rows

    def fetch_total_assessments_one_student(self, subject_id, student_id, term_id): # subject An as well
        # Pull the total assessment score on a particular student
        self.cur.execute("SELECT student.student_id, student.student_first_name, , student.student_middle_namestudent.student_last_name, subject.subject_name, SUM(assessment.score) FROM assessment JOIN student ON assessment.student_id = student.student_id JOIN enrolment ON enrolment.student_id = student.student_id JOIN subject on subject.subject_id = enrolment.subject_id WHERE student.student_id=? AND subject.subject_id=? AND assessment.term_id = ?", (student_id, subject_id, term_id))
        rows = self.cur.fetchall()
        return rows

    def fetch_total_assessments_all_students_in_subject(self, subject_id): # subject An as well
        # Pull the total assessment score on each student
        self.cur.execute("SELECT student.student_id, student.student_first_name, student.student_middle_name, student.student_last_name, subject.subject_name, SUM(assessment.score) FROM assessment JOIN student ON assessment.student_id = student.student_id JOIN enrolment ON enrolment.student_id = student.student_id JOIN subject on subject.subject_id = enrolment.subject_id WHERE subject.subject_id=? az BY student.student_id", (subject_id,))
        rows = self.cur.fetchall()
        return rows

        # Class Analytics
    def fetch_total_assessments_all_students_in_class(self, class_id):
        # Pull the total assessment score on each student
        self.cur.execute("SELECT student.student_id, student.student_first_name, student.student_middle_name, student.student_last_name, class.class_id, subject.subject_name, SUM(assessment.score) FROM class JOIN student ON class.class_id = student.class_id JOIN assessment ON assessment.student_id = student.student_id JOIN enrolment ON enrolment.student_id = student.student_id JOIN subject on subject.subject_id = enrolment.subject_id WHERE class.class_id=? GROUP BY student.student_id", (class_id,))
        rows = self.cur.fetchall()
        return rows

        # Drill down on scores. Get a bit more granular with the analytics. Descriptive Statisitcs
    def fetch_class_avg_score_all_classes(self, subject_name):
        self.cur.execute("WITH t1 AS (SELECT student.student_id, class.class_name, subject.subject_name, SUM (assessment_score) AS total_score FROM class JOIN student ON class.class_id = student.class_id JOIN assessment ON assessment.student_id = student.student_id JOIN enrolment ON enrolment.student_id = student.student_id JOIN subject on subject.subject_id = enrolment.subject_id WHERE subject.subject_name=? GROUP BY student.student_id) SELECT subject.subject_name, class.class_name, AVG (t1.total_score) GROUP BY class.class_name,", (subject_name,))
        rows = self.cur.fetchall()
        return rows

        # Case where teacher teaches same subject to multiple classes and wants to compare students' performances subject-wide

        # subject Analytics
    def fetch_avg_score_by_assessment_type(self, subject_id):
        self.cur.execute("SELECT assessment_type, AVG (assessment_score) FROM assessment WHERE assessment.subject_id=? GROUP BY assessment.type", (subject_id,))
        rows = self.cur.fetchall()
        return rows

    def fetch_min_score_by_assessment_type(self, subject_id):
        self.cur.execute("SELECT assessment_type, MIN (assessment_score) FROM assessment WHERE assessment.subject_id=? GROUP BY assessment.type", (subject_id,))
        rows = self.cur.fetchall()
        return rows

    def fetch_max_score_by_assessment_type(self, subject_id):
        self.cur.execute("SELECT assessment_type, MAX (assessment_score) FROM assessment WHERE assessment.subject_id=? GROUP BY assessment.type", (subject_id,))
        rows = self.cur.fetchall()
        return rows

        # Ideally should return 2 rows male and female with the respective average scores of each gender
    def fetch_avg_score_by_gender(self, subject_id, gender):
        self.cur.execute("WITH t1 as (SELECT student.student_id, student.gender, SUM(assessment_score) AS total_score FROM assessment JOIN student ON assessment.student_id = student.student_id JOIN enrolment ON enrolment.student_id = student.student_id JOIN subject on subject.subject_id = enrolment.subject_id WHERE subject.subject_id = ? GROUP BY student.student_id) SELECT t1.gender, AVG (t1.total_score) FROM t1 GROUP BY t1.gender", (subject_id,))
        rows = self.cur.fetchall()
        return rows

        # Leaving the subject_id and student_id entry as null with the assumption that secondary schools do not assign student or subject ids. Database set to generate it automatically
    def insert_assessment(self, subject_id, student_id, assessment_type, assessment_score):
        self.cur.execute("INSERT INTO assessment VALUES (NULL, NULL, ?, ?, ?)", (subject_id, student_id, assessment_type, assessment_score, datetime.datetime.now()))
        self.conn.commit()

    def update_assessment(self, assessment_id, assessment_type, assessment_score):
        self.cur.execute("UPDATE assessment SET assessment_type = ?, assessment_score = ? WHERE assessment.assessment_id= ?", (assessment_type, assessment_score, assessment_id))
        self.conn.commit()

    def remove_assessment(self, assessment_id):
        self.cur.execute("DELETE FROM assessment WHERE assessment.assessment_id=?", (assessment_id,))
        self.conn.commit()

    # Close connection with database
    def __del__(self):
        self.conn.close()

db = Database('models/teacher.db')

# Instantiate database
def main():
    db = db
    db.conn = sqlite3.connect('models/teacher.db', detect_types=sqlite3.PARSE_DECLTYPES |
                                                  sqlite3.PARSE_COLNAMES)

    '''
    db.cur.execute("SELECT * FROM assessment")
    rows = db.cur.fetchall()
    print(rows)
    db.conn.commit()

    db.cur = db.conn.cursor()
    db.cur.execute("BEGIN TRANSACTION;"),
    #db.cur.execute("DROP TABLE assessmen;"),

    db.cur.execute("""
            CREATE TABLE IF NOT EXISTS assessment (
                    assessment_id INTEGER NOT NULL PRIMARY KEY,
                    subject_id INTEGER NOT NULL,
                    term_id INTEGER NOT NULL,
                    student_id INTEGER NOT NULL,
                    description TEXT NOT NULL,
                    score INTEGER NOT NULL,
                    max_score INTEGER NOT NULL,
                    date TEXT NOT NULL,
                    FOREIGN KEY (subject_id) REFERENCES subject (subject_id),
                    FOREIGN KEY (student_id) REFERENCES student (student_id)
                    );"""),



    db.cur.execute("DROP TABLE assessmena;"),
    #db.cur.execute("ALTER TABLE assessmen RENAME TO assessment"),
    db.cur.execute("PRAGMA foreign_key_check;"),
    db.cur.execute("COMMIT;"),
    db.conn.commit()
    '''
    # To add columns to db, add self.cur.execute functions here and run this program directly
    # Affected tables must have their insert and and update queries adjusted accordingly and select queries if necessary
    # Foreign keys must reference either primary key columns or columns with unique constraints
if __name__ == '__main__':
    main()
