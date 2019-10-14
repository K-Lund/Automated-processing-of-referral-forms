#---------------------------------------------------------------------------------
#   IADS data science summer school
#   Team: Pink Penguin
#   Company challenge: PROVIDE
#---------------------------------------------------------------------------------
#   The following script monitors an email account and downloads pdf attachments
#   from the incoming emails.
#---------------------------------------------------------------------------------

#Import libraries
import imaplib
import os
import email
import email.utils
import time

#-------Connect to email account--------
def login():
    
    #Promt user to enter email (ex: iadschallenge@outlook.com)
    email_user=input('Email:')
    #Promt user to enter password (ex: PinkPenguin)
    email_pass=input('Password:')

    #Set up the connection
    mail=imaplib.IMAP4_SSL("outlook.office365.com",993) #host and port
    mail.login(email_user,email_pass)

    #Get a link to the email
    return mail

#-------Search inbox--------
def search(mail):

    #Select the inbox folder
    mail.select('Inbox')
    #Search the inbox for emails
    result,data=mail.uid('search', None, 'ALL')
    
    #Get a list of their unique ids
    return data[0].split()

#-------Define function to download the email attachment--------
def download_attachment(mail,current_id,main_directory):
    
    #Location to save files
    #attachment_directory='/Users/kblg/documents/Datascience/summerschool/PinkPenguin/Originals/'
    attachment_directory=main_directory+'Originals/'
    
    #Access email
    result,data=mail.uid('fetch', current_id, '(RFC822)')
    msg=email.message_from_bytes(data[0][1])
    
    #Assign a filename based on when the email was received
    emailtime=email.utils.parsedate(msg['Date'])
    fileName=time.strftime("%Y%m%d-%H%M%S", emailtime)+'.pdf'
    #Combine directory with filename to create a path for saving the attachment
    filepath=os.path.join(attachment_directory,fileName)
    
    #Walk through the different parts of the message
    for part in msg.walk():
        #Identify a pdf attachment
        if part.get_content_type()=='application/pdf':
            #Only save the file if it does not already exist
            if not os.path.isfile(filepath) :
                #save the attachment
                file = open(filepath, 'wb')
                file.write(part.get_payload(decode=True))
                file.close()
                print("Attachment downloaded.")

    #If we didn't find and save an attachment send warning message
    if not os.path.isfile(filepath):
        print('At ',msg['Date'] ,' an email was received without a PDF attachment.')

    return filepath
