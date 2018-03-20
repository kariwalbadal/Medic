from mongoengine import *
from Disease import Disease

def init():
    db_client = connect('Health', host="localhost", port=27017)
    return db_client

def destroy(db_client):
    db_client.close()

def insertDisease(d):
    d.save()
    pass

def getDiseases(symptoms):

    objects = Disease.objects()

    result = []

    for disease in objects:

        for symptom in symptoms:

            if(symptom in disease.symptoms):

                if(disease not in result):
                    result.append(disease)

            else:
                pass

    return result

def getAllSymptomps():

    objects = Disease.objects()

    result=""

    for object in objects:

        for symptom in object.symptoms:

            if symptom not in result:
                result = result + "\n" + symptom

    return result
