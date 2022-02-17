Process to deploy the project into aws lambda:-
Initially create one lambda instance with python3.7 
Step 1: Change in function code section the belows -
 Handler:- main.handler

Step 2: install all python external in-build package to project home directory
 >> pip install -r requirements.txt -t .
 > 
Step 3: archive all folders inside the servicenow_integration folder and upload the zip file

Step 4: run it  

