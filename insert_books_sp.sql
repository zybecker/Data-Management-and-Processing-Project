use library;
/*
  Procedure: InsertBook
  Description: 
    Inserts a new book into the Books table. If the provided Author_ID does not exist in the Authors table,
    a new author is created with a randomly generated name from the RandomNames table. If the provided Genre_ID
    does not exist, a random Genre_ID between 1 and 10 is assigned. The procedure also ensures that the ISBN is unique;
    if a duplicate ISBN is provided, a new one is generated. Additionally, the procedure inserts a record into the
    Books_Authors table to link the book with its author, and it adds a copy of the book into the Copy table with
    a randomly assigned availability status between 'checked_out' and 'available'.

  Parameters:
    p_title VARCHAR(255): The title of the book.
    p_author_id INT: The ID of the author. If this ID does not exist, a new author is created.
    p_genre_id INT: The ID of the genre. If this ID does not exist, a random valid Genre_ID is assigned.
    p_isbn VARCHAR(13): The ISBN of the book. If the provided ISBN already exists, a new one is generated.
    p_publication_year DATE: The publication year of the book.

  Usage:
    CALL InsertBook('Sample Book Title', 1, 2, '1234567890123', '2021-01-01');
*/

DELIMITER //

CREATE PROCEDURE InsertBook(IN p_title VARCHAR(255), IN p_author_id INT, IN p_genre_id INT, IN p_isbn VARCHAR(13), IN p_publication_year DATE)
BEGIN
    DECLARE new_author_id INT;
    DECLARE new_genre_id INT;
    DECLARE new_isbn VARCHAR(13);
    DECLARE new_book_id INT;
    DECLARE random_first_name VARCHAR(255);
    DECLARE random_last_name VARCHAR(255);
    DECLARE availability_status VARCHAR(50);

    -- Check if the author exists
    IF (SELECT COUNT(*) FROM Authors WHERE Author_ID = p_author_id) = 0 THEN
        -- Generate random author name
        SELECT FirstName INTO random_first_name FROM RandomNames ORDER BY RAND() LIMIT 1;
        SELECT LastName INTO random_last_name FROM RandomNames ORDER BY RAND() LIMIT 1;

        -- Insert new author
        INSERT INTO Authors (First_Name, Last_Name) VALUES (random_first_name, random_last_name);
        SET new_author_id = LAST_INSERT_ID();
    ELSE
        SET new_author_id = p_author_id;
    END IF;

    -- Check if the genre exists, if not, select a random genre_id between 1 and 10
    IF (SELECT COUNT(*) FROM Genre WHERE Genre_ID = p_genre_id) = 0 THEN
        SET new_genre_id = FLOOR(1 + RAND() * 10);  -- Random genre_id between 1 and 10
    ELSE
        SET new_genre_id = p_genre_id;
    END IF;

    -- Ensure ISBN is unique
-- Check if ISBN is provided and unique
	IF p_isbn IS NULL OR p_isbn = '' OR (SELECT COUNT(*) FROM Books WHERE ISBN = p_isbn) > 0 THEN
    -- Generate a new 13-digit ISBN
		SET new_isbn = LPAD(FLOOR(RAND() * 1000000000000), 13, '0');
		WHILE (SELECT COUNT(*) FROM Books WHERE ISBN = new_isbn) > 0 DO
			SET new_isbn = LPAD(FLOOR(RAND() * 1000000000000), 13, '0');
    END WHILE;
	ELSE
		SET new_isbn = p_isbn;
	END IF;

    -- Insert book
    INSERT INTO Books (Title, Author_ID, Genre_ID, ISBN, Publication_Year) VALUES (p_title, new_author_id, new_genre_id, new_isbn, p_publication_year);
    SET new_book_id = LAST_INSERT_ID();

    -- Link book and author
    INSERT INTO Books_Authors (BooksBook_ID, AuthorsAuthor_ID) VALUES (new_book_id, new_author_id);

    -- Insert a copy of the book
    SET availability_status = 'Available';
    INSERT INTO Copy (Book_ID, Availability_Status) VALUES (new_book_id, availability_status);

END //
DELIMITER ;

-- CHECK FOR VERIFICATION
CALL InsertBook('Harry Potter', 0, 0, '', '2021-02-01');
-- SELECT * FROM Books ORDER BY Book_ID DESC LIMIT 1;
-- SELECT * FROM Books_Authors WHERE BooksBook_ID = (SELECT MAX(Book_ID) FROM Books);
-- SELECT * FROM Copy WHERE Book_ID = (SELECT MAX(Book_ID) FROM Books);
 -- select * From Books;
 -- select * From Copy;
 
select * from checkouts;

select * from books;

select * from copy;


CALL DeleteBookCopy(2);
