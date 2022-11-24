#My goal with this script, is to learn how to connect to databases through python and create, modify and delete tables
##through this same software.

#1. Connecting into your Db2 SQL Database
#2. Statements through python
#3. Using Pandas to retrieve data
#4. SQL Magic
#5. Analyzing Data with Python
##5.1 Backslash "\" for splitting lines of queries
#6. Working with real world data


#1. Connecting into your Db2 SQL Database

#To connect your Python to a IBM Db2 SQL database, first, we need to install these modules.


pip install --force-reinstall ibm_db==3.1.0 ibm_db_sa==0.3.3

pip uninstall sqlalchemy==1.4 -y && pip install sqlalchemy==1.3.24

pip install ipython-sql

#Import the ibm_db module

import ibm_db


#After all of this, we need to input the data given in the service credential

dsn_hostname = "815fa4db-dc03-4c70-869a-a9cc13f33084.bs2io90l08kqb1od8lcg.databases.appdomain.cloud" # e.g.: "54a2f15b-5c0f-46df-8954-7e38e612c2bd.c1ogj3sd0tgtu0lqde00.databases.appdomain.cloud"
dsn_uid = "wnj26777"        # e.g. "abc12345"
dsn_pwd = "mNnuqxtKF55Y1upI"      # e.g. "7dBZ3wWt9XN6$o0J"

dsn_driver = "{IBM DB2 ODBC DRIVER}"
dsn_database = "BLUDB"            # e.g. "BLUDB"
dsn_port = "30367"                # e.g. "32733"
dsn_protocol = "TCPIP"            # i.e. "TCPIP"
dsn_security = "SSL"              #i.e. "SSL"


#The following script to login into your database has NOT been written by me. So just DON'T modify the code to make it work

#DO NOT MODIFY THIS CELL. Just RUN it with Shift + Enter
#Create the dsn connection string
dsn = (
    "DRIVER={0};"
    "DATABASE={1};"
    "HOSTNAME={2};"
    "PORT={3};"
    "PROTOCOL={4};"
    "UID={5};"
    "PWD={6};"
    "SECURITY={7};").format(dsn_driver, dsn_database, dsn_hostname, dsn_port, dsn_protocol, dsn_uid, dsn_pwd,dsn_security)

#print the connection string to check correct values are specified
print(dsn)


#DO NOT MODIFY THIS CELL. Just RUN it with Shift + Enter
#Create database connection

try:
    conn = ibm_db.connect(dsn, "", "")
    print ("Connected to database: ", dsn_database, "as user: ", dsn_uid, "on host: ", dsn_hostname)

except:
    print ("Unable to connect: ", ibm_db.conn_errormsg() )


#To retrieve metadata for the database server
server = ibm_db.server_info(conn)

print ("DBMS_NAME: ", server.DBMS_NAME)
print ("DBMS_VER:  ", server.DBMS_VER)
print ("DB_NAME:   ", server.DB_NAME)


#To retrieve Metadata for the Database Client / Driver
client = ibm_db.client_info(conn)

print ("DRIVER_NAME:          ", client.DRIVER_NAME)
print ("DRIVER_VER:           ", client.DRIVER_VER)
print ("DATA_SOURCE_NAME:     ", client.DATA_SOURCE_NAME)
print ("DRIVER_ODBC_VER:      ", client.DRIVER_ODBC_VER)
print ("ODBC_VER:             ", client.ODBC_VER)
print ("ODBC_SQL_CONFORMANCE: ", client.ODBC_SQL_CONFORMANCE)
print ("APPL_CODEPAGE:        ", client.APPL_CODEPAGE)
print ("CONN_CODEPAGE:        ", client.CONN_CODEPAGE)



#Finally, remember to always close your connection after using your Data base.
ibm_db.close(conn)



#2. Statements through python

#Example 1: We will now run a code to create a table.

ibm_db.exec_immediate(conn,
                      "CREATE TABLE Trucks(serial_no varchar(20) PRIMARY KEY NOT NULL,"
                      " model VARCHAR(20) NOT NULL, "
                      "Manufacturer VARCHAR(20) NOT NULL,"
                      "Engine_size VARCHAR(20) NOT NULL, "
                      "Truck_Class VARCHAR(20) NOT NULL );")


#Next step is to insert data into our table.

stmt= ibm_db.exec_immediate(conn, "INSERT INTO Trucks(serial_no, model, manufacturer, Engine_size, Truck_Class) "
                                  "VALUES('A1234', 'Lonestar', 'International Trucks', 'Cummins ISX15', 'Class 8');")


#Then, we fetch our data.

tofetch=ibm_db.exec_immediate(conn, "SELECT * FROM Trucks")

ibm_db.fetch_both(tofetch)

#Example 2: create an Instructor Table and insert data. Then, fetch the data

ibm_db.exec_immediate(conn, "CREATE TABLE Instructor(ID INTEGER NOT NULL,"
                            "Fname VARCHAR(20), "
                            "Lname VARCHAR(20),"
                            "City VARCHAR(20),"
                            "Ccode CHARACTER(5));")

ibm_db.exec_immediate(conn, "INSERT INTO Instructor(ID, Fname, Lname, City, Ccode)"
                            "VALUES(1, 'Rav', 'Ahuja', 'TORONTO', 'CA'),"
                            "(2, 'Raul', 'Chong', 'MARKHAM', 'CA'),"
                            "(3, 'Hima', 'Vasudevan', 'Chicago', 'US');")


#Then, we fetch our data.

tofetch2=ibm_db.exec_immediate(conn, "SELECT * FROM Instructor")

ibm_db.fetch_both(tofetch2)


#3. Using Pandas to retrieve data
#Import Pandas  and the ibm_db_dbi Modules
import pandas
import ibm_db_dbi
pconn = ibm_db_dbi.Connection(conn)


#Example 3: Retrieve all the data from the first table on the first example.
df= pandas.read_sql('SELECT * FROM Trucks', pconn)

df


#Example 4: Retrieve all data from the second table on the second example.

df1 = pandas.read_sql('SELECT * FROM Instructor', pconn)

df1

df1.shape

#AS ALWAYS, CLOSE CONNECTION

ibm_db.close(conn)






#4. SQL Magic
#The goal now is to learn how to use SQL Magic.
##SQL magic is basically a term for special commands that start with an "%" sign.
###One % followed by an "sql" will read the selected line as a SQL command.
###Two %% followed by an "sql" will read the entire cell as SQL commands.

#The following code is needed to load the SQL magic and to connect to the Data Base.

%load_ext sql

%sql ibm_db_sa://wnj26777:mNnuqxtKF55Y1upI@815fa4db-dc03-4c70-869a-a9cc13f33084.bs2io90l08kqb1od8lcg.databases.appdomain.cloud:30367/bludb?security=SSL


#Creating a table to work with: We start with the SQL magic to apply to the whole code.

%%sql

CREATE TABLE INTERNATIONAL_STUDENT_TEST_SCORES (
	country VARCHAR(50),
	first_name VARCHAR(50),
	last_name VARCHAR(50),
	test_score INT
);
INSERT INTO INTERNATIONAL_STUDENT_TEST_SCORES (country, first_name, last_name, test_score)
VALUES
('United States', 'Marshall', 'Bernadot', 54),
('Ghana', 'Celinda', 'Malkin', 51),
('Ukraine', 'Guillermo', 'Furze', 53),
('Greece', 'Aharon', 'Tunnow', 48),
('Russia', 'Bail', 'Goodwin', 46),
('Poland', 'Cole', 'Winteringham', 49),
('Sweden', 'Emlyn', 'Erricker', 55),
('Russia', 'Cathee', 'Sivewright', 49),
('China', 'Barny', 'Ingerson', 57),
('Uganda', 'Sharla', 'Papaccio', 55),
('China', 'Stella', 'Youens', 51),
('Poland', 'Julio', 'Buesden', 48),
('United States', 'Tiffie', 'Cosely', 58),
('Poland', 'Auroora', 'Stiffell', 45),
('China', 'Clarita', 'Huet', 52),
('Poland', 'Shannon', 'Goulden', 45),
('Philippines', 'Emylee', 'Privost', 50),
('France', 'Madelina', 'Burk', 49),
('China', 'Saunderson', 'Root', 58),
('Indonesia', 'Bo', 'Waring', 55),
('China', 'Hollis', 'Domotor', 45),
('Russia', 'Robbie', 'Collip', 46),
('Philippines', 'Davon', 'Donisi', 46),
('China', 'Cristabel', 'Radeliffe', 48),
('China', 'Wallis', 'Bartleet', 58),
('Moldova', 'Arleen', 'Stailey', 38),
('Ireland', 'Mendel', 'Grumble', 58),
('China', 'Sallyann', 'Exley', 51),
('Mexico', 'Kain', 'Swaite', 46),
('Indonesia', 'Alonso', 'Bulteel', 45),
('Armenia', 'Anatol', 'Tankus', 51),
('Indonesia', 'Coralyn', 'Dawkins', 48),
('China', 'Deanne', 'Edwinson', 45),
('China', 'Georgiana', 'Epple', 51),
('Portugal', 'Bartlet', 'Breese', 56),
('Azerbaijan', 'Idalina', 'Lukash', 50),
('France', 'Livvie', 'Flory', 54),
('Malaysia', 'Nonie', 'Borit', 48),
('Indonesia', 'Clio', 'Mugg', 47),
('Brazil', 'Westley', 'Measor', 48),
('Philippines', 'Katrinka', 'Sibbert', 51),
('Poland', 'Valentia', 'Mounch', 50),
('Norway', 'Sheilah', 'Hedditch', 53),
('Papua New Guinea', 'Itch', 'Jubb', 50),
('Latvia', 'Stesha', 'Garnson', 53),
('Canada', 'Cristionna', 'Wadmore', 46),
('China', 'Lianna', 'Gatward', 43),
('Guatemala', 'Tanney', 'Vials', 48),
('France', 'Alma', 'Zavittieri', 44),
('China', 'Alvira', 'Tamas', 50),
('United States', 'Shanon', 'Peres', 45),
('Sweden', 'Maisey', 'Lynas', 53),
('Indonesia', 'Kip', 'Hothersall', 46),
('China', 'Cash', 'Landis', 48),
('Panama', 'Kennith', 'Digance', 45),
('China', 'Ulberto', 'Riggeard', 48),
('Switzerland', 'Judy', 'Gilligan', 49),
('Philippines', 'Tod', 'Trevaskus', 52),
('Brazil', 'Herold', 'Heggs', 44),
('Latvia', 'Verney', 'Note', 50),
('Poland', 'Temp', 'Ribey', 50),
('China', 'Conroy', 'Egdal', 48),
('Japan', 'Gabie', 'Alessandone', 47),
('Ukraine', 'Devlen', 'Chaperlin', 54),
('France', 'Babbette', 'Turner', 51),
('Czech Republic', 'Virgil', 'Scotney', 52),
('Tajikistan', 'Zorina', 'Bedow', 49),
('China', 'Aidan', 'Rudeyeard', 50),
('Ireland', 'Saunder', 'MacLice', 48),
('France', 'Waly', 'Brunstan', 53),
('China', 'Gisele', 'Enns', 52),
('Peru', 'Mina', 'Winchester', 48),
('Japan', 'Torie', 'MacShirrie', 50),
('Russia', 'Benjamen', 'Kenford', 51),
('China', 'Etan', 'Burn', 53),
('Russia', 'Merralee', 'Chaperlin', 38),
('Indonesia', 'Lanny', 'Malam', 49),
('Canada', 'Wilhelm', 'Deeprose', 54),
('Czech Republic', 'Lari', 'Hillhouse', 48),
('China', 'Ossie', 'Woodley', 52),
('Macedonia', 'April', 'Tyer', 50),
('Vietnam', 'Madelon', 'Dansey', 53),
('Ukraine', 'Korella', 'McNamee', 52),
('Jamaica', 'Linnea', 'Cannam', 43),
('China', 'Mart', 'Coling', 52),
('Indonesia', 'Marna', 'Causbey', 47),
('China', 'Berni', 'Daintier', 55),
('Poland', 'Cynthia', 'Hassell', 49),
('Canada', 'Carma', 'Schule', 49),
('Indonesia', 'Malia', 'Blight', 48),
('China', 'Paulo', 'Seivertsen', 47),
('Niger', 'Kaylee', 'Hearley', 54),
('Japan', 'Maure', 'Jandak', 46),
('Argentina', 'Foss', 'Feavers', 45),
('Venezuela', 'Ron', 'Leggitt', 60),
('Russia', 'Flint', 'Gokes', 40),
('China', 'Linet', 'Conelly', 52),
('Philippines', 'Nikolas', 'Birtwell', 57),
('Australia', 'Eduard', 'Leipelt', 53)



#If you want to use a Python Variable in your SQL statement, apply  a ":" prefix" to the name of that python variable.

country="Canada"
%sql SELECT * FROM international_student_test_scores WHERE country= :country


#We can assign our results of a query to a Python Variable, just like we do when creating a Variable in Python.
##We will do a query to know the test scores accumulated by frequency.


test_score_distribution = %sql SELECT test_score AS "TestScore", COUNT(*) AS "Frequency" from INTERNATIONAL_STUDENT_TEST_SCORES GROUP BY test_score;

test_score_distribution


#Now, we will convert the query results into a DataFrame

dataframe= test_score_distribution.DataFrame()

#With matplotlib and seaborn, we will create a beautiful bar plot.
import matplotlib.pyplot as plt


import seaborn

plot = seaborn.barplot(x='testscore',y='frequency', data=dataframe)

plt.show()

#PUUUM, done.


#5. Analyzing data with Python

#For this example, we will use the Chicago socioeconomic data.
#First, we will connect to the data base.
%load_ext sql

%sql ibm_db_sa://wnj26777:mNnuqxtKF55Y1upI@815fa4db-dc03-4c70-869a-a9cc13f33084.bs2io90l08kqb1od8lcg.databases.appdomain.cloud:30367/bludb?security=SSL

#Then, we will create a PD dataframe from the source CSV

import pandas

chicago_socioeconomic_data = pandas.read_csv('https://data.cityofchicago.org/resource/jcxq-k9xf.csv')

#Finally, we use the "--persist" command in SQL magic to simplify the process of creating a table from a Pandas DF
%sql --persist chicago_socioeconomic_data

#Example 1: Count the rows in the dataset

%sql SELECT COUNT(*) FROM chicago_socioeconomic_data;


#Example 2: Count areas in Chicago where "hardship_index" is greater than 50.0

%sql SELECT COUNT(*) FROM chicago_socioeconomic_data WHERE hardship_index > 50.0;


#Example 3: Select the maximum value of the hardship index in the dataset

%sql SELECT MAX(hardship_index) FROM chicago_socioeconomic_data;


#Example 4: Select the community area with the highest harship index

%sql SELECT community_area_name FROM chicago_socioeconomic_data WHERE hardship_index = (SELECT MAX(hardship_index) FROM chicago_socioeconomic_data);


#Example 5: Show the Chicago community areas with per-capita incomes greater than $60.000

%sql SELECT community_area_name FROM chicago_socioeconomic_data WHERE per_capita_income_ > 60000;


#Example 6: Create a Scatter Plot using the "per_capita_income_" and the "hardship_index" variables.
import matplotlib.pyplot as plt


import seaborn
variables= %sql SELECT per_capita_income_ AS "PerCapitaIncome", hardship_index AS "HardshipIndex" FROM chicago_socioeconomic_data;
plot2= seaborn.scatterplot(x='percapitaincome', y='hardshipindex', data=variables.DataFrame())
plot2.show
#Example 7: use the Describe Method to obtain summary statistics from the DF

chicago_socioeconomic_data.describe(include='all')

#Example 7: Obtain the index/row number of the maximum value of the Hardship Index

chicago_socioeconomic_data['hardship_index'].idxmax()

seaborn.jointplot(x='percapitaincome', y='hardshipindex', data= variables.DataFrame())

seaborn.join


#5.1 Backslash "\" for splitting lines of queries

#To split queries when using the single % sign, use a backslash "\"

%sql SELECT COUNT(*), test_score FROM international_student_test_scores \
    GROUP BY test_score


#To get the list of tables or catalog tables to query the list of tables and their properties, you will need to check
##your Database Management System's documentation.

#In the case of DB2, the SELECT statement must include "syscat tables". In SQL Server its INFORMATION_SCHEMA.TABLES
##and in ORACLE it's ALL_TABLES or USER_TABLES.

#Example 8: retrieve a list of tables and their properties

%sql SELECT * FROM syscat.tables

#This will return too many tables.

#When using the * for the query from the syscat.tables, the system will return all the properties of the tables.

#When one is interested in the creation time, for example, to retrieve a specific table from a specific time,
##one could obtain the creation time, the tabhschema (Table creator) and tabname to retrieve the name of a table created
###at a specific time.



#Example 9: retrieve a smaller amount of data excluding system tables with the tables list and properties.

%sql SELECT tabschema, tabname, create_time FROM syscat.tables \
    WHERE LOWER(tabschema) = 'wnj26777';

#The tabschema or who created the table, contained upper case letters. Some queries need to be made case insensitive in
##order to get our data.
###To make this query case insensitive, we had to add the LOWER() statement to successfully find our data.



#To retrieve the names of the columns, use the syscat.columns. This is useful if you don't remember a name of a column


#Example 10: Retrieve all the column names from the Petrescue table. Be aware of case sensitivity. This will
##only work in DB2

%sql SELECT * FROM syscat.columns
 WHERE LOWER(tabname)='petrescue';


#Example 11: get the specific properties of the columns in the Petrescue table, like datatype and length of that
##datatype in DB2.

%sql SELECT DISTINCT(name), coltype, length FROM sysibm.syscolumns \
    WHERE LOWER(tbname)='petrescue'



#6. Working with real world data

#We will now work on a database that has been directly uploeaded with the DB2 LOAD tool.
##The database will be named SCHOOL and it shows all school level performance data used for the School Report Cards
###from the 2011-2012 school year.

#First, load the SQL magic and connect to the database as follows:

%load_ext sql

%sql ibm_db_sa://wnj26777:mNnuqxtKF55Y1upI@815fa4db-dc03-4c70-869a-a9cc13f33084.bs2io90l08kqb1od8lcg.databases.appdomain.cloud:30367/bludb?security=SSL



#Exercise 1: check if the table creation was successful:

%sql SELECT * FROM syscat.tables \
    WHERE tabschema LIKE 'WN%'

#More specifically
%sql SELECT tabname FROM syscat.tables \
    WHERE tabschema LIKE 'WN%' AND LOWER(tabname)='schools';

#Yes, it was created.



#Exercise 2: Count the number of columns in the schools table.

%%sql SELECT COUNT(*) FROM syscat.columns
    WHERE TaBNAME='SCHOOLS';

#or

%%sql SELECT COUNT(*) FROM sysibm.syscolumns
    WHERE TBNAME='SCHOOLS'

#Exercise 3: Query for all the column names and their datatypes and length from the SCHOOLS table.

%%sql SELECT DISTINCT(name), coltype, length FROM sysibm.syscolumns
    WHERE tbname='SCHOOLS'

#or
%sql select COLNAME, TYPENAME, LENGTH from SYSCAT.COLUMNS \
    where TABNAME = 'SCHOOLS'


#Exercise 4: Count each elementary schools in the dataset.

%%sql SELECT COUNT(*) FROM schools
    WHERE "Elementary, Middle, or High School" = 'ES'






#Exercise 5: select the highest safety score

%sql SELECT MAX(safety_score) FROM schools;


#Exercise 6: Select the schools with the highest safety score.

%sql SELECT Name_of_school, safety_score FROM schools \
    WHERE safety_score= (SELECT MAX(safety_score) FROM schools)


#Exercise 7: select the top 10 schools with highest "average_student_attendance"

%sql SELECT Name_of_school, average_student_attendance FROM schools \
    WHERE average_student_attendance IS NOT NULL\
    ORDER BY average_student_attendance DESC LIMIT 10;


#Exercise 8: Select the lowest 5 schools in Average Student Attendance in ascending order

%sql SELECT Name_of_school, average_student_attendance FROM schools \
    WHERE average_student_attendance IS NOT NULL \
    ORDER BY average_student_attendance ASC LIMIT 5;

#OR

%sql SELECT Name_of_school, average_student_attendance FROM schools \
    WHERE average_student_attendance IS NOT NULL \
    ORDER BY average_student_attendance ASC FETCH FIRST 5 ROWS ONLY;



#Exercise 9: Remove the '%' sign from te result showed in the exercise.

#I don't have % signs in my db. Anyways:
%sql SELECT Name_of_school, REPLACE(average_student_attendance, '%', '') FROM schools \
    WHERE average_student_attendance IS NOT NULL \
    ORDER BY average_student_attendance ASC FETCH FIRST 5 ROWS ONLY;



#Exercise 10: Name schools with Average_student_attendance lower than 70%
%sql SELECT name_of_school, average_student_attendance FROM schools \
    WHERE average_student_attendance < 70 AND average_student_attendance IS NOT NULL

#Exercise 11: Obtain the total college enrollment for each community area

%sql SELECT community_area_name, SUM(college_enrollment__number_of_students_) AS enrollment_number FROM schools \
    GROUP BY community_area_name


#Exercise 12: Obtain the 5 community areas with least college enrollment

%sql SELECT community_area_name, SUM(college_enrollment__number_of_students_) AS enrollment_number FROM schools \
    GROUP BY community_area_name \
    ORDER BY enrollment_number ASC\
    LIMIT 5

#Exercise 13: Write a query that returns the community area which has college enrollment of 4364

%sql SELECT hardship_index FROM chicago_socioeconomic_data cd, schools cps \
    WHERE cd.ca= CPS.community_area_number \
    AND college_enrollment__number_of_students_ = 4368

#Exercise 14: select the hardship index from the community area with the school with highest enrollemnt

%sql SELECT hardship_index FROM chicago_socioeconomic_data cd, schools cps \
    WHERE cd.ca = cps.community_area_number \
    AND college_enrollment__number_of_students_ = (SELECT MAX( college_enrollment__number_of_students_) FROM schools)

%sql select ca, community_area_name, hardship_index from chicago_socioeconomic_data \
   where ca in \
   ( select community_area_number from schools order by college_enrollment__number_of_students_ desc limit 1 )




