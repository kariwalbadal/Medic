from flask_api import FlaskAPI
from flask import request
from dbutils import init, getDiseases, destroy
from classifier import classifier

app = FlaskAPI(__name__)

@app.route('/')
def example():
    return "API For Health APP"

@app.route('/api/analyse', methods=['POST'])
def analyze():

    body = request.data
    db_client = init()
    print(body)
    symptom_list = body['symptoms']
    all_disease = getDiseases(symptom_list)
    potential_disease = classifier(all_disease, symptom_list)
    destroy(db_client)
    return {"disease":potential_disease}


if __name__ == "__main__":
    app.run(debug=True)