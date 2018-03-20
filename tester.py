from classifier import classifier
from Disease import  Disease
from dbutils import getDiseases, init
init()

all = getDiseases(['nausea','headache','fever','abdominal pain'])

classifier(all, ['nausea','headache','fever','abdominal pain'])
