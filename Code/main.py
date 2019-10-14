#---------------------------------------------------------------------------------
#   IADS data science summer school
#   Team: Pink Penguin
#   Company challenge: PROVIDE
#---------------------------------------------------------------------------------
#   The following script
#   -monitors an email account
#   -downloads incoming transferral forms in pdf form
#   -saves the information in a database
#---------------------------------------------------------------------------------

#-------Imports--------
from email_functions import *
from analyse_document import *
import re
main_directory='/content/gdrive/My Drive/iads/PinkPenguin/'

#-------Connect to email account--------
mail=login()

#-------Import the ID of the most recently read email--------
file = open("readmail.txt","r")
Nread_id = int(file.read())
file.close()

#-------Monitor for new emails--------

try:
    while True:

        #Search for emails
        id_list = search(mail)

        #Loop through emails
        for i in range(1,len(id_list)):
            
            #Current email ID
            current_id=id_list[-i]
            Ncurrent_id=int(re.findall('\d+',str(id_list[-i]))[0])
            
            #Evaluate whether the email is new
            if Ncurrent_id>Nread_id:
                
                #Access and download attachment
                filepath=download_attachment(mail,current_id,main_directory)
            
                #Process and save data recorded in the attachment
                if os.path.isfile(filepath):
                    processfile(filepath,main_directory)
            
            else:
                break
    
        #Update the ID of the most recently read email
        read_id=id_list[-1]
        Nread_id=int(re.findall('\d+',str(read_id))[0])
        
        #Save the ID of the most recently read email
        file = open("readmail.txt","w")
        file.write("%s" % Nread_id)
        file.close()
        
        #Wait a minute before checking the inbox again
        time.sleep(60)

#Stop program
except KeyboardInterrupt:
    
    print('The program has been stopped.')


