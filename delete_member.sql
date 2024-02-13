use library;
/*
  Procedure: DeleteMember
  Description: 
    Attempts to delete a member from the library database. Before deletion, it checks whether the member has any
    outstanding fines, active reservations, or active checkouts. If any of these conditions exist, the member is
    not deleted, and a message is returned indicating the reason why deletion cannot proceed. If none of these conditions
    apply, the member is deleted from the Members table, and a success message is returned.

  Parameters:
    xmember_id INT - The unique identifier for the member to be deleted.

  Preconditions:
    - Member_ID corresponds to an existing member in the Members table.
    - The Members table is correctly related to the Fines, Reservations, and Checkouts tables via foreign keys.

  Postconditions:
    - If the member has no outstanding fines, no active reservations, and no active checkouts, the member is deleted.
    - If the member cannot be deleted due to outstanding obligations, no changes are made to the database.

  Usage:
    CALL DeleteMember(37); -- Replace 37 with the actual Member_ID to be deleted.

  Returns:
    - A message indicating whether the member was successfully deleted or why the deletion could not be performed.
*/

DELIMITER //

CREATE PROCEDURE DeleteMember(IN xmember_id INT)
BEGIN
    DECLARE fines_count INT DEFAULT 0;
    DECLARE reservations_count INT DEFAULT 0;
    DECLARE checkouts_count INT DEFAULT 0;
    DECLARE member_exists INT DEFAULT 0;

    -- First, check if the member exists in the Members table
    SELECT COUNT(*) INTO member_exists FROM Members WHERE Member_ID = xmember_id;
    IF member_exists = 0 THEN
        -- If the member does not exist, return a message
        SELECT CONCAT('Member with ID ', xmember_id, ' does not exist in the database.') AS message;
    ELSE
        -- Check for outstanding fines
        SELECT COUNT(*) INTO fines_count FROM Fines WHERE Member_ID = xmember_id AND Payment_Status = 'Unpaid';
        -- Check for active reservations
        SELECT COUNT(*) INTO reservations_count FROM Reservations WHERE Member_ID = xmember_id;
        -- Check for active checkouts
        SELECT COUNT(*) INTO checkouts_count FROM Checkouts WHERE Member_ID = xmember_id AND Return_Date IS NULL;

        -- If there are no outstanding fines, reservations, or checkouts, delete the member
        IF fines_count = 0 AND reservations_count = 0 AND checkouts_count = 0 THEN
            DELETE FROM Members WHERE Member_ID = xmember_id;
            SELECT 'Member deleted successfully.' AS message;
        ELSE
            -- If there are outstanding obligations, do not delete the member
            SELECT CONCAT('Cannot delete member with ID ', xmember_id, 
                          ' as they have pending Checkout/Reservation/Fine. Please contact the member to resolve this dispute.') AS message;
        END IF;
    END IF;
END //

DELIMITER ;

CALL DeleteMember(88);
select * from members;
