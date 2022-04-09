class Student:

    # an object class representing the students taking the Computer Appreciation course
    def __init__(self, student_name, test_1_score, test_2_score, project_score, exam_score):
        self.name = student_name
        self.test_1 = test_1_score
        self.test_2 = test_2_score
        self.project = project_score
        self.exam = exam_score
        self.total_score = ""
        self.position = []


    # the following functions allow for the pulling of student scores data
    def get_name(self):
        return self.name

    def get_gender(self):
        print("Undefined")

    def get_test_1(self):
        return  self.test_1

    def get_test_2(self):
        return self.test_2

    def get_project(self):
        return self.project

    def get_exam(self):
        return self.exam

    def get_total(self):
        self.total_score = self.test_1 + self.test_2 + self.project + (self.exam/100) * 60
        return self.total_score

    # the following functions allow for the editing of student names and scores data
    def set_name(self, student_name):
        self.name = student_name

    def set_test_1(self, test_1_score):
        self.test_1 = test_1_score

    def set_test_2(self, test_2_score):
        self.test_2 = test_2_score

    def set_project(self, project_score):
        self.project = project_score

    def set_exam(self, exam_score):
        self.exam = exam_score


# the following classes inherit from the class 'Student' and are differentiated on gender
class MaleStudent(Student):

    def get_gender(self):
        return self.gender

    def set_gender(self, gender):
        self.gender = gender

class FemaleStudent(Student):

    def get_gender(self):
        return self.gender

    def set_gender(self, gender):
        self.gender = gender



# the class Course to define the course taken by the students
class Course:
    # class attribute showing number of students
    number_of_students = 0

    def __init__(self, name):
        self.name = name
        Course.number_of_students +=1 # keeps track of the students added to course. Also a way to track no. of students

        self.students = [] # list of students; empty since number of students that will be added is unknown at this point
        self.male_students = []
        self.female_students = []

# adds the male students to a separate list
    def add_male_students(self, student):
        if student.get_gender() == "male":
            self.male_students.append(student)
            return True
        return False

# adds the female students to a separate list
    def add_female_students(self, student):
        if student.get_gender() == "female":
            self.female_students.append(student)
            return True
        return False

# adds male and female students to the general list of students
    def add_students(self, student):
        # self.students = [student for student in self.male_students] might replace the below with a list comprehension
        for student in self.male_students:
            self.students.append(student)

       # worried about what happens if i implement list comp for below as above
        for student in self.female_students:
            self.students.append(student)

# calculates the average score for female students
    def get_average_score_female_students(self):
        value = 0
        for student in self.female_students:
            value += self.female_students.get_total()
        return value / len(self.female_students)

# calculates the average score for male students
    def get_average_score_male_students(self):
        value = 0
        for student in self.male_students:
            value += self.male_students.get_total()

        return value / len(self.male_students)

# calculates the total average score for all students
    def get_total_average_score_students(self):
        value = 0
        for student in self.students:
            value += self.students.get_total()

        return value / len(self.students)

    # I realised a lesson in abstraction tonight. 14th December 2021
    # The clue is to look for those functions that have barely any interaction within them with other parts like the database etc 
    # will abstract this function. create module student.py which is the class you already wrote, get position will take 3 args self, score(float), scorelist(list) 
    
# calculate each student's position in class
    def get_position(self, score, score_list):
        """
        Return the student's position in the course.

        Parameters:
        score -- student's total score (float)

        Returns:
        integer of the student's position in the course
        """

        """
        Algorithm:
        Create a list of the student's scores.
        Sort list in place in descending order.
        Count and store number of different scores in list.
        Create a dictionary of lists with integers as keys beginning from 1.
        Insert list's first score into first list in dictionary of list.
        Remove score from list.
        Compare new list's first score with dictionary's first value.
        If identical, insert score into dictionary and remove from list. Repeat as required.
        Repeat with subsequent list in dictionary of lists.
        With the dictionary of lists built, a score can now be compared with each list.
        Position is assigned based on what list the score falls.
        """
        try:
            scores = score_list
            scores.sort(reverse=True)
            # a loop to count the number of different scores in the list. This will be used to build the dictionary
            i = 0
            count = 1
            # if a score is different from the subsequent score on the list, the count increases by 1
            for i in range(len(scores) -1):
                if scores[i] != scores[i+1]:
                    count += 1
            # build dictionary phase of function starts here
            score_dict = {}
            # check if length of scores list is > 0, then initiate dictionary with first key and value
            if len(scores) > 0:
                score_dict[1] = [scores[0]]
                scores.remove(scores[0])
            # use while loop to increase size of dictionary by adding identical values if any to the first key.
            i = 1
            while i < count:

                if score_dict[i][0] == scores[0]:
                    score_dict[i].append(scores[0])
                    scores.remove(scores[0])
            # jumps to subsequent key within the dictionary after there are no more identical scores to fill in key 1.
                else:
                    i+=1
                    score_dict[i] = [scores[0]]
                    scores.remove(scores[0])
            """        
            The position location phase of this function starts here. It uses the dictionary keys to identify position of score
            If score is in first dictionary list, position = first,
            If score is in second, position = first key + length of previous list and so on
            this is so that if there are students with identical scores, their positions are the same
            and the next position awarded is reflective of that
            """
            if score in score_dict[1]:
                position_of_student = 1
            else:
                i = 1
                position_of_student = 1
                while score not in score_dict[i]:
                    position_of_student += len(score_dict[i])
                    i +=1
            return position_of_student # returns an integer
        # Error handling
        except: KeyError()


ca = Course('Computer Appreciation')