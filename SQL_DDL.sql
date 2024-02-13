use library;
-- Create Authors table
CREATE TABLE Authors (
    Author_ID INT PRIMARY KEY AUTO_INCREMENT,
    First_Name VARCHAR(255) NOT NULL,
    Last_Name VARCHAR(255) NOT NULL
);

-- Create Subscriptions table
CREATE TABLE Subscriptions (
    Subscription_ID INT PRIMARY KEY AUTO_INCREMENT,
    Subscription_Type VARCHAR(50) NOT NULL,
    Fee DECIMAL(10, 2) NOT NULL
);


-- Create Librarians table
CREATE TABLE Librarians (
    Librarian_ID INT PRIMARY KEY AUTO_INCREMENT,
    First_Name VARCHAR(255) NOT NULL,
    Last_Name VARCHAR(255) NOT NULL,
    Email VARCHAR(255) NOT NULL
);


-- Create Genre table
CREATE TABLE Genre (
    Genre_ID INT PRIMARY KEY AUTO_INCREMENT,
    Genre_Name VARCHAR(255) NOT NULL
);

-- Create Books table
CREATE TABLE Books (
    Book_ID INT PRIMARY KEY AUTO_INCREMENT,
    Title VARCHAR(255) NOT NULL,
    Author_ID INT,
    Genre_ID INT,
    ISBN VARCHAR(13),
    Publication_Year DATE,
    FOREIGN KEY (Author_ID) REFERENCES Authors(Author_ID),
    FOREIGN KEY (Genre_ID) REFERENCES Genre(Genre_ID)
);

-- Create Copy table
CREATE TABLE Copy (
    Copy_ID INT PRIMARY KEY AUTO_INCREMENT,
    Book_ID INT,
    Availability_Status VARCHAR(50) NOT NULL,
    FOREIGN KEY (Book_ID) REFERENCES Books(Book_ID)
);

-- Create Members table
CREATE TABLE Members (
    Member_ID INT PRIMARY KEY AUTO_INCREMENT,
    First_Name VARCHAR(255) NOT NULL,
    Last_Name VARCHAR(255) NOT NULL,
    Email VARCHAR(255) NOT NULL,
    Subscription_ID INT,
    FOREIGN KEY (Subscription_ID) REFERENCES Subscriptions(Subscription_ID)
);

-- Create Checkouts table
CREATE TABLE Checkouts (
    Checkout_ID INT PRIMARY KEY AUTO_INCREMENT,
    Member_ID INT,
    Copy_ID INT,
    Checkout_Date DATE,
    Due_Date DATE,
    Return_Date DATE,
    Librarian_ID INT,
    FOREIGN KEY (Member_ID) REFERENCES Members(Member_ID),
    FOREIGN KEY (Copy_ID) REFERENCES Copy(Copy_ID),
    FOREIGN KEY (Librarian_ID) REFERENCES Librarians(Librarian_ID)
);

-- Create Reviews table
CREATE TABLE Reviews (
    Review_ID INT PRIMARY KEY AUTO_INCREMENT,
    Member_ID INT,
    Book_ID INT,
    Review_Text TEXT,
    Ratings INT,
    FOREIGN KEY (Member_ID) REFERENCES Members(Member_ID),
    FOREIGN KEY (Book_ID) REFERENCES Books(Book_ID)
);

-- Create Fines table
CREATE TABLE Fines (
    Fine_ID INT PRIMARY KEY AUTO_INCREMENT,
    Member_ID INT,
    Checkout_ID INT,
    Amount DECIMAL(10, 2),
    Payment_Status VARCHAR(50) NOT NULL,
    FOREIGN KEY (Member_ID) REFERENCES Members(Member_ID),
    FOREIGN KEY (Checkout_ID) REFERENCES Checkouts(Checkout_ID)
);


-- Create Reservations table
CREATE TABLE Reservations (
    Reservation_ID INT PRIMARY KEY AUTO_INCREMENT,
    Member_ID INT,
    Copy_ID INT,
    Reservation_Date DATE,
    CheckoutsCheckout_ID INT,
    FOREIGN KEY (Member_ID) REFERENCES Members(Member_ID),
    FOREIGN KEY (Copy_ID) REFERENCES Copy(Copy_ID),
    FOREIGN KEY (CheckoutsCheckout_ID) REFERENCES Checkouts(Checkout_ID)
);

-- Create Books_Authors table
CREATE TABLE Books_Authors (
    BooksBook_ID INT,
    AuthorsAuthor_ID INT,
    PRIMARY KEY (BooksBook_ID, AuthorsAuthor_ID),
    FOREIGN KEY (BooksBook_ID) REFERENCES Books(Book_ID),
    FOREIGN KEY (AuthorsAuthor_ID) REFERENCES Authors(Author_ID)
);

CREATE TABLE Admins (
    Admin_ID INT PRIMARY KEY AUTO_INCREMENT,
    First_Name VARCHAR(255) NOT NULL,
    Last_Name VARCHAR(255) NOT NULL,
    Email VARCHAR(255) NOT NULL,
    Access_Level VARCHAR(50) NOT NULL
);


ALTER TABLE Reservations DROP FOREIGN KEY reservations_ibfk_3;

ALTER TABLE Reservations DROP COLUMN CheckoutsCheckout_ID;
