# Database-Project
please create your own branch to work on your part


Always pull the code to update your branch by running the following commands in order:<br>
  git pull master <br>
  git checkout your_branch_name <br>
  git merge origin/master <br>

Whenever making a pull request please add tarunkukreja003 as the reviewer <br>

After you have made your changes, write an appropriate commit message and push your code to YOUR BRANCH by running the following command:

git push origin your_branch_name <br>

Configuration Steps:

1. Set Up MySQl is your PC(Download, install, set up database)
2. Open MySQL Workbench, and create a new database and connect to it. In the database create a schema name app_schema and select it -> All of this has to be done on MySQL WorkBench
3. Create tables in Worbench and commands for create tables are present in Database_Project doc
4. Run the following two commands on your terminal:<br>
  
  pip3 install mysql-connector<br>
  pip3 install mysql<br>
5. In database_operations file enter the credentials of your local sql server in connectToDatabase() function <br>
6. Run customer_terminal.py and check if there are enrties in account and customer table



