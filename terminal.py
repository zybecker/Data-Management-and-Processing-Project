import mysql.connector
from mysql.connector import Error
import pandas as pd 
from sqlalchemy import create_engine, text
import sys
from sqlalchemy.orm import sessionmaker
import random
from sqlalchemy import create_engine, MetaData,\
Table, Column, Numeric, Integer, VARCHAR, update

from datetime import date
from datetime import datetime
from dateutil.relativedelta import relativedelta

host = "localhost"
database = "Library"
user = "root" # enter your username if not root
password = "<>" # enter yur password

def create_connection_string(user, password, host, database):
    return f"mysql+mysqlconnector://{user}:{password}@{host}/{database}"

def create_db_engine(user, password, host, database):
    connection_string = create_connection_string(user, password, host, database)
    engine = create_engine(connection_string)
    return engine

def admin_menu():
    while True:
        print("\nAdmin Menu:")
        print("1. Insert\n2. Update Member Info\n3. Delete\n4. View\n5. Return to Main Menu\n6. Exit")
        admin_choice = input("Select an option: ")

        if admin_choice == "1":
            admin_insert_menu()
        elif admin_choice == "2":
            admin_update_member()
        elif admin_choice == "3":
             admin_delete_menu()
        elif admin_choice == "4":
            admin_view_menu()  # This calls the view submenu
        elif admin_choice == "5":
            return  # This will return to the main menu
        elif admin_choice == "6":
            sys.exit("Exiting the system.")
        else:
            print("Invalid choice, please try again.")

def admin_update_member():
    try:
        engine = create_db_engine(user, password, host, database)
        member_id = int(input("Enter the ID of the member to update: "))

        with engine.connect() as connection:
            # Check if the member exists
            exists_query = text("SELECT COUNT(*) FROM Members WHERE Member_ID = :member_id")
            result = connection.execute(exists_query, {'member_id': member_id})
            if result.scalar() == 0:
                print("\nMember does not exist\n.")
                return

            new_subscription_id = input('Enter new subscription level for the member: ')
            new_email = input("Enter new email for the member: ")

            # Update the member's subscription ID and other fields
            update_query = text("UPDATE Members SET Email = :new_email, Subscription_ID = :new_subscription_id WHERE Member_ID = :member_id")
            connection.execute(update_query, {
                'new_email': new_email, 
                'new_subscription_id': new_subscription_id, 
                'member_id': member_id
            })

            print(f"Member updated successfully with new Subscription ID: {new_subscription_id}, new Email = {new_email}")

            connection.commit()
    
    except Exception as e:
        print(f"An error occurred: {e}")

def admin_insert_menu():
    while True:
        print("\nAdmin Insert\Add Menu:")
        print("1. Books\n2. Members\n4. Go Back\n5. Exit\n")
        view_choice = input("Select an option: ")

        if view_choice == "1":
            admin_insert_books()
        elif view_choice == "2":
            admin_insert_members()
        elif view_choice == "3":
            admin_add_librarians()
        elif view_choice == "4":
            return  # This will return to the previous menu (admin_menu)
        elif view_choice == "5":
            sys.exit("Exiting the system.")
        else:
            print("Invalid choice, please try again.")

def admin_insert_books():
    try:
        engine = create_db_engine(user, password, host, database)
        title = input("Enter book title: ")
        author_id = int(input("Enter author ID (0 if not known): "))
        genre_id = int(input("Enter genre ID (0 if not known): "))
        isbn = input("Enter ISBN (leave blank for auto-generation): ")
        publication_year = input("Enter publication year (YYYY-MM-DD): ")

        # Calling the stored procedure
        procedure_call = text("CALL InsertBook(:title, :author_id, :genre_id, :isbn, :publication_year)")
        with engine.connect() as connection:
            connection.execute(procedure_call, {
                'title': title, 
                'author_id': author_id, 
                'genre_id': genre_id, 
                'isbn': isbn, 
                'publication_year': publication_year
            })
            connection.commit()
            print("\nBook successfully added to the database. Here are the last 10 Books")
            # Fetch and display the latest member(s)
            recent_books_query = text("SELECT * FROM Books ORDER BY Book_ID DESC LIMIT 10")
            recent_books = connection.execute(recent_books_query)
            for book in recent_books:
                # Formatting the date
                formatted_date = book.Publication_Year.strftime('%Y-%m-%d') if book.Publication_Year else 'Unknown'
                print(f"({book.Book_ID}, '{book.Title}', {book.Author_ID}, {book.Genre_ID}, '{book.ISBN}', '{formatted_date}')")

    except Exception as e:
        print(f"An error occurred: {e}")

def admin_insert_members():
    try:
        engine = create_db_engine(user, password, host, database)
        first_name = input("Enter member's first name: ")
        last_name = input("Enter member's last name: ")
        email = input("Enter member's email: ")
        subscription_id = random.randint(1, 3)  # Assuming there are only 3 subscription levels

        insert_query = text("""
            INSERT INTO Members (First_Name, Last_Name, Email, Subscription_ID) 
            VALUES (:first_name, :last_name, :email, :subscription_id)
        """)
        with engine.connect() as connection:
            connection.execute(insert_query, {
                'first_name': first_name, 
                'last_name': last_name, 
                'email': email, 
                'subscription_id': subscription_id
            })
            connection.commit() 
            print("Member successfully added. Here's are the last 5 members:")

            # Fetch and display the latest member(s)
            recent_members_query = text("SELECT * FROM Members ORDER BY Member_ID DESC LIMIT 5")
            recent_members = connection.execute(recent_members_query)
            for member in recent_members:
                print(member)
    except Exception as e:
        print(f"An error occurred: {e}")

def admin_add_librarians():
    try:
        engine = create_db_engine(user, password, host, database)
        first_name = input("Enter librarian's first name: ")
        last_name = input("Enter librarian's last name: ")
        email = input("Enter librarian's email: ")

        insert_query = text("""
            INSERT INTO Librarians (First_Name, Last_Name, Email) 
            VALUES (:first_name, :last_name, :email)
        """)
        with engine.connect() as connection:
            connection.execute(insert_query, {
                'first_name': first_name, 
                'last_name': last_name, 
                'email': email
            })
            connection.commit()
            print("Librarian successfully added.")
            
            # Fetch and display the latest member(s)
            recent_librarians_query = text("SELECT * FROM Librarians ORDER BY Librarian_ID DESC LIMIT 5")
            recent_librarians = connection.execute(recent_librarians_query)
            for member in recent_librarians:
                print(member)
    except Exception as e:
        print(f"An error occurred: {e}")

def admin_view_menu():
    while True:
        print("\nAdmin View Menu:")
        print("1. Books\n2. Members\n3. Go Back\n4. Exit\n")
        view_choice = input("Select an option: ")

        if view_choice == "1":
            admin_view_books()
        elif view_choice == "2":
            admin_view_members()
        elif view_choice == "3":
            return  # This will return to the previous menu (admin_menu)
        elif view_choice == "4":
            sys.exit("Exiting the system.")
        else:
            print("Invalid choice, please try again.")

def admin_view_books():
    try:
        engine = create_db_engine(user, password, host, database)
        query = "SELECT * FROM Books"
        df = pd.read_sql(query, engine)
        print(df)
    except Exception as e:
        print(f"An error occurred: {e}")

def admin_view_members():
    try:
        engine = create_db_engine(user, password, host, database)
        query = "SELECT * FROM Members"
        df = pd.read_sql(query, engine)
        print(df)
    except Exception as e:
        print(f"An error occurred: {e}")

def admin_delete_menu():
    while True:
        print("\nAdmin Delete Menu:")
        print("1. Books\n2. Members\n3. Go Back\n4. Exit\n")
        view_choice = input("Select an option: ")

        if view_choice == "1":
            admin_delete_book_copy()
        elif view_choice == "2":
            admin_delete_member()
        elif view_choice == "3":
            return  # This will return to the previous menu (admin_menu)
        elif view_choice == "4":
            sys.exit("Exiting the system.")
        else:
            print("Invalid choice, please try again.")

def admin_delete_book_copy():
    try:
        book_id = int(input("Enter the ID of the book copy to delete: "))
        engine = create_db_engine(user, password, host, database)

        # First connection for calling stored procedure
        connection1 = engine.raw_connection()
        try:
            cursor = connection1.cursor()
            cursor.callproc("DeleteBookCopy", [book_id])

            # Fetch results from the stored procedure
            for result_set in cursor.stored_results():
                for result in result_set.fetchall():
                    print(result[0])  # Assuming the message is the first column

            connection1.commit()
        finally:
            cursor.close()
            connection1.close()

        # Second connection for fetching and displaying last 10 books
        connection2 = engine.connect()
        try:
            print("\nBook successfully deleted from the database. Here are the last 10 Books")
            recent_books_query = text("SELECT * FROM Books ORDER BY Book_ID DESC LIMIT 10")
            recent_books = connection2.execute(recent_books_query)

            for book in recent_books:
                # Formatting the date
                formatted_date = book.Publication_Year.strftime('%Y-%m-%d') if book.Publication_Year else 'Unknown'
                print(f"({book.Book_ID}, '{book.Title}', {book.Author_ID}, {book.Genre_ID}, '{book.ISBN}', '{formatted_date}')")
        finally:
            connection2.close()

    except Exception as e:
        print(f"An error occurred: {e}")

def admin_delete_member():
    cursor = None
    try:
        member_id = int(input("Enter the ID of the member to delete: "))
        engine = create_db_engine(user, password, host, database)
        connection = engine.raw_connection()
        cursor = connection.cursor()
        cursor.callproc("DeleteMember", [member_id])

        # Fetch results from the stored procedure
        for result_set in cursor.stored_results():
            for result in result_set.fetchall():
                print(result[0])  

        connection.commit()

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

def librarian_menu():
    while True:
        print("\nLibrarian Menu:")
        print("1. View\n2. Update Availability Status of Books\n3. Return to Main Menu\n4. Exit")
        choice = input("Select an option: ")

        if choice == "1":
            librarian_view_menu()
        elif choice == "2":
            librarian_update()
        elif choice == "3":
            return  # This will return to the main menu
        elif choice == "4":
            sys.exit("Exiting the system.")
        else:
            print("Invalid choice, please try again.")

def librarian_view_menu():
        while True:
            print("\nLibrarian View Menu:")
            print("1. Books\n2. Members\n3. Checkouts by Member\n4. Go Back\n5. Exit\n")
            view_choice = input("Select an option: ")

            if view_choice == "1":
                librarian_view_books()
            elif view_choice == "2":
                librarian_view_members()
            elif view_choice == "3":
                librarian_filter_by_member()
            elif view_choice == "4":
                return  # This will return to the previous menu (admin_menu)
            elif view_choice == "5":
                sys.exit("Exiting the system.")
            else:
                print("Invalid choice, please try again.")

def librarian_filter_by_member():
    cursor = None
    try:
        engine = create_db_engine(user, password, host, database)
        member_id = input("Please enter member ID: ")
        
        connection = engine.raw_connection()
        cursor = connection.cursor()

        # Execute the stored procedure
        cursor.callproc("GetMemberCheckouts", [member_id])

        # Fetch results from the stored procedure
        for result_set in cursor.stored_results():
            results = result_set.fetchall()
            if results:
                # Define column headers as per your stored procedure's SELECT statement
                columns = ['Title', 'Author_First_Name', 'Author_Last_Name', 'Checkout_Date', 'Due_Date', 'Return_Date']
                df = pd.DataFrame(results, columns=columns)
                
                # Convert date columns to datetime if not already
                df['Checkout_Date'] = pd.to_datetime(df['Checkout_Date']).dt.strftime('%Y-%m-%d')
                df['Due_Date'] = pd.to_datetime(df['Due_Date']).dt.strftime('%Y-%m-%d')
                df['Return_Date'] = pd.to_datetime(df['Return_Date']).dt.strftime('%Y-%m-%d')

                print("Checkout information for member ID", member_id)
                print(df.to_string(index=False))  # Print DataFrame without the index
            else:
                print("No checkout information found for member ID", member_id)
                
        connection.commit()

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        # Close the cursor and the connection
        if cursor:
            cursor.close()
        if connection:
            connection.close()

def librarian_view_books():
    try:
        engine = create_db_engine(user, password, host, database)
        query = "SELECT * FROM Books"
        df = pd.read_sql(query, engine)
        print(df)
    except Exception as e:
        print(f"An error occurred: {e}")

def librarian_view_members():
    try:
        engine = create_db_engine(user, password, host, database)
        query = "SELECT * FROM Members"
        df = pd.read_sql(query, engine)
        print(df)
    except Exception as e:
        print(f"An error occurred: {e}")

def librarian_update():
    try:
        engine = create_db_engine(user, password, host, database)
        meta = MetaData()
        meta.reflect(bind=engine)

        action = int(input("Are you checking out (0) or returning (1) a book? "))

        if action == 0:  # checking out book
            c_id = input("Please enter the copy ID of the book you are checking out: ")
            m_id = input("Please enter the member ID of the member checking the book out: ")

            with engine.connect() as connection:
                # Update the copy table to reflect the book is checked out
                copy_table = meta.tables['Copy']
                stmt = update(copy_table).values(Availability_Status="Checked Out").where(copy_table.c.Copy_ID == c_id)
                connection.execute(stmt)
                connection.commit()

            with engine.connect() as connection:
                # Insert a row into the checkouts table
                checkouts_table = meta.tables['Checkouts']
                statement = checkouts_table.insert().values(
                    Member_ID=m_id,
                    Copy_ID=c_id,
                    Checkout_Date=date.today(),
                    Due_Date=date.today() + relativedelta(months=1),
                    Return_Date=None,
                    Librarian_ID=random.randint(1,10)
                )
                connection.execute(statement)
                
                connection.commit()

                # Fetch the most recent insert's Checkout_ID
                checkout_df = pd.read_sql("SELECT Checkout_ID FROM Checkouts", con=engine)
                checkout_id = checkout_df["Checkout_ID"].max()
                print(f"Your checkout ID is {checkout_id}. Please save this to return the book")
                

        elif action == 1:  # returning a book
            c_id = input("Please enter the copy ID of the book you are returning: ")
            checkout_id = input("Please enter the checkout ID of the book: ")

            with engine.connect() as connection:
                # Update the copy table to reflect the book is available
                copy_table = meta.tables['Copy']
                stmt = update(copy_table).values(Availability_Status="Available").where(copy_table.c.Copy_ID == c_id)
                connection.execute(stmt)
                connection.commit()
            
            with engine.connect() as connection:
                # Update the return date in the checkouts table
                checkouts_table = meta.tables['Checkouts']
                stmt = update(checkouts_table).values(Return_Date=date.today()).where(checkouts_table.c.Checkout_ID == checkout_id)
                connection.execute(stmt)
                print(f'\nSuccessfully Returned and Return Date saved to be the present date : {date.today()}\n')

                connection.commit()

    except Exception as e:
        print(f"An error occurred: {e}")

def member_menu():
        while True:
            print("\nMember Menu:")
            print("1. View Fines\n2. Search Books\n3. Reserve Books\n4. Go Back\n5. Exit\n")
            print('All checkouts and reserves are processed by Librarians, Please Enter the Librarian menu to process Checkouts/Returns\n')
            view_choice = input("Select an option: ")

            if view_choice == "1":
                member_view_fines()
            elif view_choice == "2":
                member_book_search()
            elif view_choice == "3":
                member_reservation()
            elif view_choice == "4":
                return  # This will return to the previous menu (admin_menu)
            elif view_choice == "5":
                sys.exit("Exiting the system.")
            else:
                print("Invalid choice, please try again.")

def member_view_fines():
    try:

        engine = create_db_engine(user, password, host, database)
        
        # Prompt the user for the member ID
        member_id = int(input("Please enter your member ID: "))
        
        with engine.connect() as connection:
            # Check if the member exists
            result = connection.execute(text("SELECT COUNT(*) FROM Members WHERE Member_ID = :member_id"), {'member_id': member_id})
            member_exists = result.scalar()
            
            if member_exists == 0:
                print(f"Member with ID {member_id} does not exist.")
                return

            # If the member exists, call the stored procedure
            connection.execute(text("CALL CalculateTotalFines(:member_id, @totalFines)"), {'member_id': member_id})
            total_fines = connection.execute(text("SELECT @totalFines")).scalar()
            
            if total_fines is None:
                print(f"Member with ID {member_id} has no unpaid fines.")
            else:
                print(f"Member with ID {member_id} has unpaid fines totaling: ${total_fines:.2f}")
    
    except Exception as e:
        print(f"An error occurred: {e}")

def member_book_search():
    try:
        engine = create_db_engine(user, password, host, database)
        method = int(input("Search by Title (0), Author Last Name (1), or ISBN (2) "))

        if method == 0: # search by title
            title = input("Enter title: ")
            query = f"SELECT * FROM Books WHERE LOWER(Title) = LOWER('{title}')"
            title_df = pd.read_sql(query, con = engine)
            
            if title_df["Book_ID"].count() == 0:
                print(f"No books found with given title: {title}")
            else:
                print(title_df)
            
        elif method == 1: # by author_id
            author_name = input("Enter Authors Last Name: ")
            query = f"SELECT * FROM Books_Authors ba JOIN Books b ON ba.BooksBook_ID = b.Book_ID JOIN Authors a ON a.Author_ID = ba.AuthorsAuthor_ID WHERE LOWER(a.Last_Name) = LOWER('{author_name}')"
            
            author_df = pd.read_sql(query, con = engine)
            
            if author_df['Book_ID'].count() == 0:
                print(f"No books found for last name: {author_name} ")
            else:
                print(author_df.drop(["BooksBook_ID", "AuthorsAuthor_ID"], axis = 1))
        
        elif method == 2: #ISBN
            isbn = input("Enter the 13 digit ISBN: ")
            query = f"SELECT * FROM Books WHERE ISBN = {isbn}"
            isbn_df = pd.read_sql(query, con = engine)
            
            if isbn_df["Book_ID"].count() == 0:
                print(f"No books found with ISBN: {isbn}")
            else:
                print(isbn_df)
        else:
            print("Invalid Choice")
    except Exception as e:
        print(f"An error occurred: {e}")

def member_reservation():
    try:        
        engine = create_db_engine(user, password, host, database)
        meta = MetaData()
        meta.reflect(bind=engine)
        
        mem_id = input("Please enter your member ID: ")
        copy_id = input("Please enter the copy ID of the book you want to reserve: ")
        
        
        query = f"SELECT Availability_Status FROM COPY WHERE Copy_ID = {copy_id}"
        aval_df = pd.read_sql(query, con = engine)
        
        if aval_df["Availability_Status"][0] == "Checked Out":
            print("Cannot reserve book, already checked out")
            
        else:
            with engine.connect() as connection:
                RES = meta.tables["Reservations"]
                stmt = RES.insert().values(Member_ID = mem_id,
                                          Copy_ID = copy_id,
                                          Reservation_Date = date.today())
                connection.execute(stmt)
                
                print("Book successfuly reserved!")
            
                connection.commit()
        

        
    except Exception as e:
        print(f"An error occurred: {e}")

def main():
    while True:
        print("Welcome to the Library Management System")
        print("1. Admin\n2. Librarian\n3. Member\n4. Exit")
        choice = input("Select your role: ")

        if choice == "1":
            admin_menu()
        elif choice == "2":
            librarian_menu()
        elif choice == "3":
            member_menu()
        elif choice == "4":
            print("Exiting the system.")
            break
        else:
            print("Invalid choice, please try again.")

if __name__ == "__main__":
    main()
