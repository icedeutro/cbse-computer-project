import mysql.connector as connector
# connection and database creation
connection = connector.connect(host="localhost", user="root", passwd="andrew123")
cursor = connection.cursor()


def user_selection():
    print("""
    YOU CAN PERFORM THE FOLLOWING FUNCTIONS:1.add student info. 2. set attendance. 3. set elgiblity criteria.
     4. check elgibility. 5. room allotement. 6. delete student info
    """)
    selection = int(input("enter your selection(1, 2, 3, 4, 5 or 6:  "))
    return selection


def create_db():
    # connection and database creation
    connection = connector.connect(host="localhost", user="root", passwd="andrew123")
    cursor = connection.cursor()

    cursor.execute("create database management")
    table_creation = """ 
    create table students (
        student_id int primary key, 
        name varchar(50), 
        attendance varchar(100), 
        science_marks int, 
        math_marks int, 
        english_marks int, 
        branch varchar(100),
        semester int
    );
    """
    cursor.execute(table_creation)


def add_details():
    number_of_records = int(input("enter the number of records you want to enter : "))
    insert_query = """
    insert into students (id, name, attendance, sci_marks, math_marks, engl_marks, branch, semester)
    values (%s, %s, %s, %s, %s, %s, %s, %s)
    """

    for i in range(number_of_records):
        print("for student number: ",i+1)
        id = int(input("enter student id: "))
        name = input("enter name of student")
        attendance = input("enter details of attendance: ")
        sci_marks = int(input("enter students science marks: "))
        math_marks = int(input("enter students math marks: "))
        engl_marks = int(input("enter students english marks: "))
        branch = input("enter students branch(software, mechanical, electrical or aerospace): ")
        semester = int(input("enter which semester the student is currently in"))
        stu_data = [id, name, attendance, sci_marks, math_marks, engl_marks, branch, semester]
        cursor.executemany(insert_query, stu_data)
        connection.commit()
    print("process finished successfully")


def set_attendance(student_id):
    attendance = input("enter details about students attendance: ")
    update_query = """
    update students
    set attendance = %s
    where student_id = %s
    """
    data_to_update = (attendance, student_id)
    cursor.executemany(update_query, data_to_update)
    connection.commit()


def set_eligibility():
    minmath = int(input("enter the minimum math marks for eligibility : "))
    minsci = int(input("enter the minimum science marks for eligibility : "))
    mineng = int(input("enter the minimum english marks for eligibility : "))
    sem = int(input("enter the semester the student needs to be in: "))
    branch = input("enter the branch the student needs to be in: ")
    minmarks = [minmath, minsci, mineng, sem, branch.lower()]
    print("eligibility criteria set successfully")
    return minmarks


def check_eligibility(criteria):
    eligible_students = []
    if len(criteria) != 3:
        print("""
        Error in criteria given. Please enter a list with math, science, english marks and semester and branch in order
        """)
    else:
        math = criteria[0]
        science = criteria[1]
        english = criteria[2]
        sem = criteria[3]
        branch = criteria[4]
        check_query = """
        SELECT student_id from students
        WHERE maths_marks >= %s AND science_marks >= %s AND english_marks >=%s AND semester = %s AND branch = %s
        """
        cursor.execute(check_query, (math, science, english, sem, branch.lower()))
        eligible_students = cursor.fetchall()
        print("number of students eligible are: ", len(eligible_students), "they are: ")
        for i in eligible_students:
            j = 1
            print(j, ". ", i)
            j += 1
    return eligible_students
