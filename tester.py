from classifier import classifier
from disease import Disease

cold = Disease('cold', ['nausea', 'mild fever', 'headache', 'vomiting', 'body ache', 'throat ache', 'cough'], 9000, 4000, 500)
typhoid = Disease('typhoid', ['nausea', 'rash', 'weakness', 'abdominal pain', 'high fever', 'headache', 'constipation',
                              'confusion', 'diarrhoea','vomiting'], 7000, 5000, 4693)
flu = Disease('flu', ['nausea', 'headache', 'fatigue','body ache', 'cough','sore throat','fever', 'gastrointestinal disorder'], 1000, 800, 200)
diseases = [cold, typhoid, flu]
classifier(diseases, ['throat ache', 'mild fever', 'nausea', 'constipation'])
