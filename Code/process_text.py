#---------------------------------------------------------------------------------
#   IADS data science summer school
#   Team: Pink Penguin
#   Company challenge: PROVIDE
#---------------------------------------------------------------------------------
#   The following script describes how text is treated, categorised and stored
#---------------------------------------------------------------------------------
import re

def normalize(text):
    
    text_without_special_chars = re.sub("[^A-Za-z0-9/\n()]+", ' ', text)
    normalized_text = text_without_special_chars.strip().lower()
    
    return normalized_text

#Create empty dictionary
def create_dict():

    #import categories for dictionary
    dictfile=open(r'dictionary.txt','r')
    dictlist = dictfile.read()
    dictfile.close()
    categories = dictlist.split(",")

    return dict.fromkeys(categories, None)

def sort_text(text,referral_info):
    #identify relevant text
    if ":" in text:
        
        #split text into field name and field value
        field_name = text.split(':')[0]
        field_value = text.split(':')[1]
        
        #normalise text
        normalized_field_name = normalize(field_name)
        normalized_field_value = normalize(field_value)
        
        #special cases where linebreaks are replaced by comma
        linespace_to_comma_fields = ["allergies and sensitivities",
                                     "current repeat templates for prescriptions",
                                     "address and postcode"]
                                     
        #replace linebreak by comma
        if normalized_field_name in linespace_to_comma_fields:
            linespace_removed_field_value = normalized_field_value.replace("\n", ", ")
        
        #replace linebreak by space
        else:
            linespace_removed_field_value = normalized_field_value.replace("\n", " ")
        
        #store field value information in dictionary
        if normalized_field_name in referral_info.keys():
            referral_info[normalized_field_name] = linespace_removed_field_value

    return referral_info

# for appending data from dictionary to a csv file
def dict_to_csv(input_dict, file_name):
    import csv
    
    with open(file_name + ".csv", 'a', newline='') as f:
        
        w = csv.DictWriter(f, input_dict.keys())
        if f.tell() == 0:
            w.writeheader()
            w.writerow(input_dict)
        else:
            w.writerow(input_dict)


def identify_fields(textinput,referral_info):

    #identify whether this field has been labelled previously
    if referral_info["reason for referral"]=="next.":
        
        #save information
        referral_info["reason for referral"] = textinput

    #identify special field and label it
    elif 'reason for referral' in textinput:
        #signal that next section is the "reason for referral"
        referral_info["reason for referral"] = "next."
    
    #treat field as a normal case and analyse the text
    else:
        referral_info=sort_text(textinput,referral_info)
    
    return referral_info


