{\rtf1\ansi\ansicpg1252\cocoartf1561\cocoasubrtf600
{\fonttbl\f0\fswiss\fcharset0 Helvetica;}
{\colortbl;\red255\green255\blue255;}
{\*\expandedcolortbl;;}
\paperw11900\paperh16840\margl1440\margr1440\vieww16680\viewh11180\viewkind0
\pard\tx566\tx1133\tx1700\tx2267\tx2834\tx3401\tx3968\tx4535\tx5102\tx5669\tx6236\tx6803\pardirnatural\partightenfactor0

\f0\fs24 \cf0 STRUCTURE:\
1. Code folder contains:\
	main.py - run this to monitor check and process emails \
	email_functions.py - monitors email account and downloads pdf attachments \
	analyse_document.py - converts a pdf to images and finds text information\
	process_text.py - describes how text is processed, categorised and stored \
	dictionary.txt - a list of every database category (every field in the referral forms)\
	readmail.txt - contains the id number of the most recently read email\
2. Database folder contains a csv file with the information retrieved from the referral forms (end result).\
3. Originals folder stores the downloaded pdf attachments from the email labelled using the timestamp of when the email was received. \
4. Temp_files folder is used to temporarily store images of the split pdf pages whilst they are being processed.  \
\
INITIAL SETUP:\
1. Update \'93main_directory\'94 in main.py to a directory containing the folders \'93Code\'94, \'93Database\'94, \'93Originals\'94 and \'93Temp_files\'94\
2. Write 0 in readmail.txt \
3. Specify in main.py how often you would like the email account to be searched by changing the number in \'93time.sleep(SECONDS)\'94\
\
TO USE: \
1. run main.py \
2. login \
ctr+c in terminal to stop the program \
\
}
