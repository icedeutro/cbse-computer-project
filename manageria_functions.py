import mysql.connector as connector
# connection and database creation
connection = connector.connect(host="localhost", user="root", passwd="andrew123")
cursor = connection.cursor()


def user_selection():
    print("""
    YOU CAN PERFORM THE FOLLOWING FUNCTIONS:1.add student info. 2. set attendance. 3. set elgiblity criteria.
     4. check elgibility. 5.  delete student info
    """)
    selection = int(input("enter your selection(1, 2, 3, 4, or 5):  "))
    return selection


def create_db():
    #WORKS
    # connection and database creation
    try:
        connection = connector.connect(host="localhost", user="root", passwd="andrew123")
        cursor = connection.cursor()

        cursor.execute("""
        create database management;
        """)

    except:
        print("database already created")

def create_table():
    #WORKS
    try:
        connection = connector.connect(host="localhost", user="root", passwd="andrew123", database="management")
        cursor = connection.cursor()
        table_creation = """
                        create table if not exists students(
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
    except connector.Error as err:
        print(f"Error: {err}")

    cursor.close()
    connection.close()

def add_details():
    #WORKS
    connection = connector.connect(host="localhost", user="root", passwd="andrew123", database="management")
    cursor = connection.cursor()
    number_of_records = int(input("enter the number of records you want to enter : "))
    insert_query = """
    insert into students (student_id, name, attendance, science_marks, math_marks, english_marks, branch, semester)
    values (%s, %s, %s, %s, %s, %s, %s, %s);
    """

    for i in range(number_of_records):
        print("for student number: ",i+1)
        id = (input("enter student id: "))
        name = input("enter name of student: ")
        attendance = input("enter details of attendance: ")
        sci_marks = (input("enter students science marks: "))
        math_marks = (input("enter students math marks: "))
        engl_marks = (input("enter students english marks: "))
        branch = input("enter students branch(software, mechanical, electrical or aerospace): ")
        semester = (input("enter which semester the student is currently in: "))
        stu_data = [id, name, attendance, sci_marks, math_marks, engl_marks, branch, semester]
        try:
            cursor.execute(insert_query, stu_data)
        except connector.Error as err:
            print(f"Error: {err}")
            print("PLEASE MAKE SURE YOU HAVE ENTERED ALL THE DATA CORRECTLY")
            print("NOTE: id -> int, name -> string, attendance->string, all marks->int, branch -> string, semester->int")

        cursor.close()
        connection.commit()


def set_attendance(student_id):
    #WORKS
    connection = connector.connect(host="localhost", user="root", passwd="andrew123", database="management")
    cursor = connection.cursor()
    attendance = input("enter details about students attendance: ")
    try:
        update_query = """
           update students
           set attendance = %s
           where student_id = %s
           """
        data_to_update = [(attendance, student_id)]
        cursor.executemany(update_query, data_to_update)
    except connector.Error as err:
        print(f"Error: {err}")

    connection.commit()


def check_eligibility(criteria):
    #works
    connection = connector.connect(host="localhost", user="root", passwd="andrew123", database="management")
    cursor = connection.cursor()
    eligible_students = []
    if len(criteria) != 5:
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
        SELECT student_id, name from students
        WHERE math_marks >= %s AND science_marks >= %s AND english_marks >=%s AND semester = %s AND branch = %s
        """
        cursor.execute(check_query, (math, science, english, sem, branch.lower()))
        eligible_students = cursor.fetchall()
        print("number of students eligible are: ", len(eligible_students), "they are: ")
        for i in eligible_students:
            j = 1
            print(j, ".", i)
            j += 1
    return eligible_students


def remove_details():
    #works
    id = int(input("enter the id of the student record to be removed: "))
    confirmation = input("you are about to delete the record of given student id, if you are sure enter 'yes': ")
    if confirmation.lower() == "yes" or confirmation.lower() =='y':
        connection = connector.connect(host="localhost", user="root", passwd="andrew123", database="management")
        cursor = connection.cursor()
        del_query = "delete from students where student_id = %s"
        cursor.execute(del_query, [id])
        connection.commit()
        print("record deleted successfully!")
    else:
        print("Ok! going back now")

