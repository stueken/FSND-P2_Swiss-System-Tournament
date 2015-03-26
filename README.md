# Database Schema and Methods: Swiss System Tournament Framework
Project to create a database and method framework to realize a Swiss system tournament. Thereby, some database
programming skills in PostgreSQL and Python are exercised.

# Detailed Description
There are three files and an extra_credit folder with additional three files with the same names. In both cases, the
three files have the following functions:
- tournament.sql: Here the database with its tables, primary and foreign keys as well as its views is defined. This file
needs to be imported once to the database (command "\i tournament.sql") to set up the whole underlying database model.
- tournament.py: This file contains all methods with its queries which can be applied on the database.
- tournament_test.py: This file constains methods to test the methods in tournament.py and its results.

The three files in the base folder include only the code which is needed to meet all minimum specifiations for the
project like deletion and registering of players, reporting matches and finding pairings for the next Swiss system
tournament round. Additionally, the files in the extra_credit folder contain more complex code to exceed the 
specifications of the project and meet 3 out 4 extra credit options. These are:
- An uneven amount of players is allowed for a tournament. The odd player who doesn't get a match partner gets a 
free bye-win, which he can only get once in a tournament.
- Draws are possible and are reported separately.
- Multiple tournaments are supported. No tournament, match or player has to be deleted from the database. Also, players
in the database have to be explicitly registered for a tournament.

Additionally, primary and foreign key constraints are implemented in the database schema.

NOTE: The database model for tournament_extra (extra credit) can be accessed through the 'Issues'-tab on the right. 

# Requirements
The project has been run from a vagrant virtual machine, but basically the main requirements are the following:
- Python 2.7
- PostgreSQL

# Running Instructions
1. Change either to the base or the extra_credit directory
2. In the command prompt start the PostgreSQL database by typing 'psql'
3. From there create a new database, e.g. by typing 'CREATE DATABASE tournament;'
4. Connect to the new database by typing '\c tournament'
5. Import the database model and its views by typing '\i tournament.sql'
6. Exit from the database with CTRL+d
7. Finally, start the test file with 'python tournament_test.py'
