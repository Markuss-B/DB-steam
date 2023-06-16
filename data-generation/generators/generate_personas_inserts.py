# CREATE TABLE Persona (
#     ID int PRIMARY KEY FOREIGN KEY REFERENCES Lietotājs(ID),
#     Vārds nvarchar(50) NOT NULL,
#     Uzvārds nvarchar(50) NOT NULL,
#     DzimšanasDatums date NOT NULL,
#     EPasts nvarchar(100) NOT NULL,
#     Parole nvarchar(100) NOT NULL,
# 	NorēķinuAdreseID int NOT NULL FOREIGN KEY REFERENCES NorēķinuAdrese(ID)
# );
from faker import Faker
import random

faker = Faker('lv_LV')


id_count = 85
adrs_count = 30

# Create a list to store the SQL statements
insert_statements = []
statement = "INSERT INTO Persona (ID, Vārds, Uzvārds, DzimšanasDatums, EPasts, Parole, NorēķinuAdreseID) VALUES"
insert_statements.append(statement)

# Function to create an INSERT statement
def create_insert_statement(id, vards, uzvards, dzimsanasdatums, epasts, parole, norekinuadreseid):
    statement = f"\t({id}, '{vards}', '{uzvards}', '{dzimsanasdatums}', '{epasts}', '{parole}', {norekinuadreseid}),"
    return statement

for id in range(1000, 1000+id_count):
    vards = faker.first_name()
    uzvards = faker.last_name()
    dzimsanasdatums = faker.date_of_birth(minimum_age=18, maximum_age=100)
    epasts = faker.email()
    parole = faker.password()
    norekinuadreseid = random.randint(1, adrs_count)
    insert_statements.append(create_insert_statement(id, vards, uzvards, dzimsanasdatums, epasts, parole, norekinuadreseid))

insert_statements[-1] = insert_statements[-1][:-1] + ';'

# Write the statements to a file
with open('inserts\\personas_inserts.sql', 'w', encoding='utf-8') as f:
    for statement in insert_statements:
        f.write(statement + '\n')