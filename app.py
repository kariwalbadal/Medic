from flask_api import FlaskAPI

app = FlaskAPI(__name__)

@app.route('/')
def example():
    return "API For Health APP"

@app.route('/api/analyse', methods=['POST'])
def analyze():

    body = request.data

    return body


if __name__ == "__main__":
    app.run(debug=True)