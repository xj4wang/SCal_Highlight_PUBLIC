import csv
import os
import json
from collections import defaultdict

cord_uid_to_text = defaultdict(list)

# open the file
with open('metadata.csv') as f_in:
    reader = csv.DictReader(f_in)
    for row in reader:
    
        # access some metadata
        cord_uid = row['cord_uid']
        title = row['title']
        abstract = row['abstract']
        authors = row['authors']
        journal = row['journal']
        publish_time = row['publish_time']
        
        # check if the file already exists, if yes take the one with the most recent date
        if cord_uid in cord_uid_to_text:
            old_publish_time = cord_uid_to_text[cord_uid][0].get('publish_time')
            if publish_time < old_publish_time:
                print(cord_uid + ": " + publish_time + ", " + old_publish_time)
                continue


        # save for later usage
        cord_uid_to_text[cord_uid].append({
            'title': title,
            'abstract': abstract,
            'authors': authors,
            'journal': journal,
            'publish_time' : publish_time
        })
        
        # create and write to file       
        f = open("cord-19_test/" + cord_uid, "w")
        
        f.write("title: " + title + "\n")
        f.write("\n")
        f.write ("publish_time: " + publish_time + "\n")
        f.write ("authors: " + authors + "\n")
        f.write ("journal: " + journal + "\n")
        f.write ("\n")        
        f.write(abstract + "\n")
        
        f.close()
        
