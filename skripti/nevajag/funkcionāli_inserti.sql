-- Jauns profils
DECLARE @NewUserID int;

-- Insert a new user into the Lietotājs table
INSERT INTO Lietotājs (Niks) VALUES ('Niks');

-- Get the ID of the newly inserted user
SET @NewUserID = SCOPE_IDENTITY();

-- Now you can use @NewUserID to insert a row into the Persona table
INSERT INTO Persona (ID, Vārds, Uzvārds, DzimšanasDatums, EPasts, Parole, NorēķinuAdreseID)
VALUES (@NewUserID, 'YourName', 'YourSurname', 'YourBirthday', 'YourEmail', 'YourPassword', 'YourAddressID');