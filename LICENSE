CREATE VIEW BookDetails AS
SELECT B.Book_ID, B.Title, CONCAT(A.First_Name, ' ', A.Last_Name) AS Author, G.Genre_Name, B.ISBN, B.Publication_Year
FROM Books B
JOIN Authors A ON B.Author_ID = A.Author_ID
JOIN Genre G ON B.Genre_ID = G.Genre_ID;


CREATE VIEW FineDetails AS 
SELECT F.Fine_ID, M.First_Name AS Member_First_Name, M.Last_Name AS Member_Last_Name, B.Title AS Book_Title,
F.Amount, F.Payment_Status, C.Checkout_Date, C.Due_Date, C.Return_Date FROM Fines F
JOIN Members M ON F.Member_ID = M.Member_ID
JOIN Checkouts C ON F.Checkout_ID = C.Checkout_ID
JOIN Copy CO ON C.Copy_ID = CO.Copy_ID
JOIN Books B ON CO.Book_ID = B.Book_ID;


DELIMITER //
CREATE PROCEDURE GetAvailableBooks(IN genreName VARCHAR(255))
BEGIN
	SELECT B.Title, A.First_Name AS Author_First_Name, A.Last_Name AS Author_Last_Name, G.Genre_Name, C.Availability_Status
    FROM Books B
    JOIN Authors A ON B.Author_ID = A.Author_ID
    JOIN Genre G ON B.Genre_ID = G.Genre_ID
    JOIN Copy C ON B.Book_ID = C.Book_ID
    WHERE G.Genre_Name = genreName AND C.Availability_Status = 'Available';
END //
DELIMITER ;


DELIMITER //
CREATE PROCEDURE GetMemberCheckouts(IN memberId INT)
BEGIN
    SELECT B.Title, A.First_Name AS Author_First_Name, A.Last_Name AS Author_Last_Name, C.Checkout_Date, C.Due_Date, C.Return_Date
    FROM Checkouts C
    JOIN Members M ON C.Member_ID = M.Member_ID
    JOIN Copy CO ON C.Copy_ID = CO.Copy_ID
    JOIN Books B ON CO.Book_ID = B.Book_ID
    JOIN Authors A ON B.Author_ID = A.Author_ID
    WHERE M.Member_ID = memberId;
END //
DELIMITER ;


DELIMITER //
CREATE PROCEDURE CalculateTotalFines(IN memberId INT, OUT totalFines DECIMAL(10, 2))
BEGIN
    SELECT SUM(F.Amount) INTO totalFines FROM Fines F
    WHERE F.Member_ID = memberId AND F.Payment_Status = 'Unpaid';
END //
DELIMITER ;


DELIMITER //
CREATE FUNCTION GetAverageBookRating(bookId INT) RETURNS DECIMAL(3, 2)
BEGIN
    DECLARE avgRating DECIMAL(3, 2);
    SELECT AVG(R.Ratings) INTO avgRating
    FROM Reviews R
    WHERE R.Book_ID = bookId;
    RETURN COALESCE(avgRating, 0);
END //
DELIMITER ;


DELIMITER //
CREATE FUNCTION IsBookAvailable(bookId INT) RETURNS BOOLEAN
BEGIN DECLARE availability BOOLEAN;
    SELECT CASE WHEN COUNT(*) > 0 THEN TRUE ELSE FALSE END INTO availability
    FROM Copy
    WHERE Book_ID = bookId AND Availability_Status = 'Available';
    RETURN availability;
END //
DELIMITER ;


DELIMITER //
CREATE FUNCTION GetMemberSubscriptionFee(memberId INT) RETURNS DECIMAL(10, 2)
BEGIN DECLARE subscriptionFee DECIMAL(10, 2);
	SELECT S.Fee INTO subscriptionFee FROM Members M
    JOIN Subscriptions S ON M.Subscription_ID = S.Subscription_ID
    WHERE M.Member_ID = memberId;
    RETURN COALESCE(subscriptionFee, 0);
END //
DELIMITER ;


DELIMITER //
CREATE TRIGGER UpdateMemberTotalFine
AFTER INSERT ON Fines
FOR EACH ROW BEGIN
    DECLARE totalFine DECIMAL(10, 2);
    SELECT COALESCE(SUM(Amount), 0) INTO totalFine
    FROM Fines
    WHERE Member_ID = NEW.Member_ID;
    UPDATE Members
    SET Total_Fine = totalFine
    WHERE Member_ID = NEW.Member_ID;
END //
DELIMITER ;
