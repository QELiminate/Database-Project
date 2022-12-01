# QueueEliminationSystem

Steps to run the project:

1. Set Up MySQl is your PC(Download, install, set up database)
2. Open MySQL Workbench, and create a new database and connect to it. In the database create a schema by the name "app_schema" and select it
3. Create tables in Workbench using the create commands mentioned in https://docs.google.com/document/d/1BakATbty1SU_b_gbNLNo9xTxzI-OOmsd0AGQE274K3g/edit?usp=sharing
4. Download and Install python3 and pip3 in your system
5. Clone the master branch of this repository by clicking on the green Code button and then copy the https link, then open terminal on your system and navigate to a directory where you would like to clone the project. Then type the following commands in the terminal:
   
   <br>
   git clone https://github.com/QELiminate/Database-Project.git
   <br><br>
   cd Database-Project
   <br><br>
   pip3 install -r requirements.txt
   <br> <br>
6. Insert data in the tables created using the Insert Commands mentioned in https://docs.google.com/document/d/1BakATbty1SU_b_gbNLNo9xTxzI-OOmsd0AGQE274K3g/edit?usp=sharing
  
7. Go to the database_operations.py file in the Database-Project directory and in connectToDatabase() function replace 'your_username' and 'your_password' with your local SQL username and password respectively <br>
8. Run the following command:
    <br> <br>
    python3 customer_terminal.py <br> <br>
9. Once done with working with all the functions in customer_terminal.py go ahead and run the following command to work with functions that restaurant has <br>
    <br>
    python3 restaurant_terminal.py
