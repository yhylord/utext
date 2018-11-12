#TF = query term occurrence/ total terms
#IDF = (TotalNumber of Documents/ number of documents with term in it)
#Final Weight = TF * IDF

import math
import requests
import bs4 as BeautifulSoup
Soup = BeautifulSoup.BeautifulSoup



#copy pasted a list from other file runtime bad programming srry
docs = ['BCAL', 'Bus Routes', 'Center for Students in Recovery', 'CMHC - Crisis Line', 'CMHC - General',
        'CMHC - Groups ', 'CMHC - Mind Body Labs', 'Family Life Services', 'Forty Acres Pharmacy',
        'Free Self Defense Classes-UTPD', 'Gender and Sexuality Center', 'Hornslink',
        'Interpersonal Violence Peer Support Program ', 'Legal Services', 'Longhorn Automative Program',
        'Multicultural Engagement Center', 'New Student Services', 'New Student Services- Longhorn Way',
        'New Student Services- Rise 2018', 'Office of Health Promotions', 'Office of Sorority & Fraternity Life',
        'Ombuds Office', 'Parking and Transportation Services Bike Service', 'RecSports - Fitness and Wellness',
        'RecSports - General', 'RecSports - IM Sports', 'RecSports - Sport Clubs', 'RecSports- Texercise', 'Sanger Learning Center',
        'Services for Students with Disabilities', 'Student Activities', 'Student Conduct & Academic Integrity', 'Student Emergency Services ( SES )',
        'Student Government', 'Student Veteran Services', 'SURE Ride', 'SURE Walk', 'University Health Services - Allergies and Immunizations',
        'University Health Services - General Medicine', 'University Health Services - Nurse Advice Line', 'University Health Services - Nutrition Services',
        'University Health Services - Physical Therapy', 'University Health Services - Sexual Assualt Forensic Exams',
        'University Health Services - Sports Medicine', 'University Health Services - STI Testing', 'University Health Services - Travel Health',
        "University Health Services - Women's Health", 'University Writing Center', 'UT Copy and Print', 'UT Leadership and Ethics Institute',
        'VAV', 'Graduation Help Desk', 'CMHC - Thrive App', 'Title IX - Report Incident', 'Texas Athletics', 'Title IX - Report Incident (1)']



def tf_idf(query):
    total_docs = 0.0
    contain_docs = 0.0
    idf = 0

    for doc in docs:

        filename = "TextData/" + doc + ".txt"
        data = open(filename,'r')
        contain = False
        occ = 0.0
        total_terms = 0.0


        for word in data.read().split():
            total_terms = total_terms + 1.0
            if query.lower()==word.lower():
                contain = not contain
                occ = occ + 1.0
        if total_terms!=0.0:
            tf_scores[doc] = occ#/total_terms      #DIFFERENT CHANGE !!
        if contain:
            contain_docs = contain_docs + 1.0
        total_docs = total_docs + 1.0
    if contain_docs!=0.0:
     idf = math.log(total_docs/contain_docs)
    return idf




# putting TF_IDF scores to document (update elastic serach column fields)


#use elastic search to narrow documents !



#send back pointers to fullfillment !


#make tfidf branch






numQuery = input("How many words ")
query = []
scores = []

for x in range(0,numQuery):
    tf_scores = {}
    tf_idf_scores = {}
    y = raw_input("Enter Query: ")
    query.append(y)
    ourIDF = tf_idf(y)
    for key in tf_scores:
        tf_idf_scores[key] = tf_scores[key] * ourIDF
    print(tf_idf_scores)
    print(ourIDF)
    scores.append(tf_idf_scores)

total_TFIDF_scores = {}

for key in scores[0]:
    val = 0
    for di in scores:
        val+=di[key]
    total_TFIDF_scores[key] = val


total_TFIDF_scores = sorted(total_TFIDF_scores.iteritems(), key=lambda (k,v): (v,k),reverse=True)


print("Top Scores")
for x in range(0,5):
    print(total_TFIDF_scores[x])












