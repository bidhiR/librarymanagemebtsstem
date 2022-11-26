import sqlite3
import os

# Classes
class library():
    def __init__(self, isbn, book_name, number_of_copies):              #constructor
        self.isbn = isbn
        self.book_name = book_name
        self.number_of_copies = number_of_copies


class student():
    def __init__(self, rollno, name, borrowed_status, borrowed_days):       #constructor
        self.rollno = rollno
        self.name = name
        self.borrowed_status = borrowed_status
        self.borrowed_days = borrowed_days


connLib = sqlite3.connect("library.sqlite")
connStd = sqlite3.connect("student.sqlite")
curLib = connLib.cursor()
curStd = connStd.cursor()

createLibrary_script = '''
CREATE TABLE library (
    ISBN INT PRIMARY KEY,
    book_name VARCHAR(30),
    number_of_copies INT
)
'''

createStudent_script = '''
CREATE TABLE student (
    rollno INT PRIMARY KEY,
    name VARCHAR(30),
    borrowed_status VARCHAR(6),
    borrowed_days INT
)'''
# curLib.execute(createLibrary_script)

# curStd.execute(createStudent_script)

# numberOfStudents = int(input("Enter the number of students: "))
# for i in range(numberOfStudents):
#     rollno = int(input("Enter the roll number of students: "))
#     name = input("Enter the name of student: ").upper()
#     borrowed_status = "FALSE"
#     borrowed_days = 0
#     newStudent = student(rollno, name, borrowed_status, borrowed_days)
#     insertStudentScript = '''
#     INSERT INTO student VALUES (?,?,?,?)'''
#     curStd.execute(insertStudentScript, (newStudent.rollno, newStudent.name,
#                    newStudent.borrowed_status, newStudent.borrowed_days))
#     print("Successfully added into the student table\n")

print("WELCOME TO THE LIBRARY MANAGEMENT SYSTEM\n")
print("1. Add Book\n")
print("2. Borrow Book\n")
print("3. Return Book\n")
print("4. Modify\n")
print("5. Search Book\n")
print("6. Display all books\n")

choice = int(input("Choose your option: "))
#Exception handling
try:
    if (choice == 1):
        os.system("cls")
        numberOfBooks = int(input("enter the number of books to add: "))
        for i in range(numberOfBooks):
            isbn = int(input("Enter the ISBN of book: "))
            book_name = input("Enter the book name: ").upper()
            number_of_copies = int(input("Enter the number of copies: "))
            newBook = library(isbn, book_name, number_of_copies)
            insertBookScript = '''
            INSERT INTO library VALUES (?,?,?)
            '''
            curLib.execute(insertBookScript, (newBook.isbn,
                           newBook.book_name, newBook.number_of_copies))
            print("Successfully added into the table\n")

    elif (choice == 2):
        os.system("cls")
        student_borrowing_rollno = int(input("Enter your student rollno: "))

        studentBorrowChecker = f'''
        SELECT name, borrowed_status
        FROM student
        WHERE rollno = {student_borrowing_rollno} AND borrowed_status = "FALSE"'''
        borrowingStudent = curStd.execute(studentBorrowChecker)
        studentDump = curStd.fetchall()
        studentList = []
        for borrowingStudent in studentDump:
            studentList.append(borrowingStudent)

        if (len(studentList) != 0):
            studentBorrowUpdate = f'''
            UPDATE student
            SET borrowed_status = "TRUE"
            WHERE rollno = {student_borrowing_rollno} AND borrowed_status = "FALSE"'''
            curStd.execute(studentBorrowUpdate)

            book_to_borrow = int(
                input("Enter the ISBN of book you want to borrow: "))
            borrowBookUpdate = f'''
            UPDATE library 
            SET number_of_copies = number_of_copies - 1 
            WHERE ISBN = {book_to_borrow} AND number_of_copies>0
            '''
            curLib.execute(borrowBookUpdate)
            print("Successfully borrowed the book.")

        else:
            print("no such student exists, or has already borrowed the book")

    elif (choice == 3):
        print("Return Book part")
        os.system("cls")
        student_borrowing_rollno = int(input("Enter your student rollno: "))
        studentBorrowChecker = f'''SELECT name,
        borrowed_status 
        FROM student
        WHERE rollno = {student_borrowing_rollno} AND borrowed_status = "TRUE"'''
        borrowingStudent = curStd.execute(studentBorrowChecker)
        studentDump = curStd.fetchall()
        studentList = []
        for borrowingStudent in studentDump:
            studentList.append(borrowingStudent)

        if (len(studentList) != 0):
            studentBorrowUpdate = f'''
            UPDATE student
            SET borrowed_status = "FALSE"
            WHERE rollno = {student_borrowing_rollno} AND borrowed_status = "TRUE"'''
            curStd.execute(studentBorrowUpdate)

            book_to_return = int(
                input("Enter the ISBN of book you want to return: "))
            returnBookUpdate = f'''
            UPDATE library 
            SET number_of_copies = number_of_copies + 1 
            WHERE ISBN = {book_to_return}
            '''
            curLib.execute(returnBookUpdate)
            print("Successfully returned the book.")

        else:
            print("no such student exists, or hasnt borrowed the book")

    elif (choice == 4):
        os.system("cls")
        print("1. Modify Student\n")
        print("2. Modify Library")
        modify_choice = int(input("Choose you option: "))

        try:
            os.system("cls")
            if (modify_choice == 1):
                student_rollno = int(
                    input("Enter the roll no of student to modify: "))
                newBorrowedDays = int(input("Enter the new borrowed days: "))
                studentModify = f'''
                UPDATE student
                SET borrowed_days = {newBorrowedDays}
                WHERE rollno = {student_rollno} AND borrowed_status = "TRUE"
                '''
                curStd.execute(studentModify)
                print("Successfully modified the borrowed days")

            elif (modify_choice == 2):
                book_isbn = int(
                    input("Enter the ISBN of book to modify number of copies: "))
                newNumberOfCopies = int(
                    input("Enter the new number of copies: "))
                bookModify = f'''
                UPDATE library
                SET number_of_copies = {newNumberOfCopies}
                WHERE ISBN = {book_isbn}'''
                curLib.execute(bookModify)
                print("Successfully modified the number of copies")
            else:
                raise ValueError
        except ValueError:
            print("invalid choice")

    elif (choice == 5):
        bookToSearch = input("Enter the name of book to search: ").upper()
        bookSearch = f'''
        SELECT ISBN, book_name, number_of_copies
        FROM library
        WHERE book_name = "{bookToSearch}"
        '''
        searchedBook = curLib.execute(bookSearch)
        bookDump = curLib.fetchall()
        os.system("cls")
        print("BOOK DETAILS: ")
        print("ISBN\tBOOK NAME\tCOPIES:\n")
        for searchedBook in bookDump:
            print(f"{searchedBook[0]}\t{searchedBook[1]}\t\t{searchedBook[2]}")

    elif (choice == 6):
        selectall = '''
        SELECT * FROM library'''
        bookDump = curLib.execute(selectall)
        os.system("cls")
        print("ALL THE LIBRARY LISTINGS ARE: \n")
        print("ISBN\tNAME OF BOOK\tNUMBER OF COPIES\n")
        for row in bookDump:
            print(f"{row[0]}\t{row[1]}\t\t{row[2]}")
    else:
        raise ValueError
except ValueError:
    print("You entered the wrong option")

connLib.commit()
connLib.close()
connStd.commit()
connStd.close()
