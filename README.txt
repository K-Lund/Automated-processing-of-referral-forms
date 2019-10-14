STRUCTURE (if these folders do not exist they must be created):
1. Code folder contains:
	main.py - run this to monitor check and process emails 
	email_functions.py - monitors email account and downloads pdf attachments 
	analyse_document.py - converts a pdf to images and finds text information
	process_text.py - describes how text is processed, categorised and stored 
	dictionary.txt - a list of every database category (every field in the referral forms)
	readmail.txt - contains the id number of the most recently read email
2. Database folder contains a csv file with the information retrieved from the referral forms (end result).
3. Originals folder stores the downloaded pdf attachments from the email labelled using the timestamp of when the email was received. 
4. Temp_files folder is used to temporarily store images of the split pdf pages whilst they are being processed.  \

INITIAL SETUP:
1. Replace "main_directory" in main.py with the path to a directory containing the folders "Code", "Database", "Originals" and "Temp_files"
2. Write 0 in readmail.txt 
3. Specify in main.py how often you would like the email account to be searched by changing the number in "time.sleep(SECONDS)"

TO USE: 
1. run main.py 
2. login 
ctr+c in terminal to stop the program 
