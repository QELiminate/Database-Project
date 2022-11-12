# Database-Project

Whenever making a pull request please add tarunkukreja003 as the reviewer
whenever pulling, run the following commands:<br>
  git pull master <br>
  git checkout your_branch_name <br>
  git merge origin/master <br>

please create your own branch to work on your part

Configuration Steps:

1. Set Up MySQl is your PC(Download, install, set up database)
2. Open MySQL Workbench, and create a new database and connect to it. In the database create a schema name app_schema and select it -> All of this has to be done on MySQL WorkBench
3. Create tables in Worbench and commands for create tables are present in Database_Project doc
4. Run the following two commands on your terminal:<br>
  
  pip3 install mysql-connector<br>
  pip3 install mysql<br>
5. In database_operations file enter the credentials of your local sql server in connectToDatabase() function

6. Run customer_terminal.py and check if there are enrties in account and customer table



