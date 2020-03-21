import flask
from flask import request, jsonify
import bioprocessor
import json

p = bioprocessor.BioProcessor()

app = flask.Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    return '''<h1>librAIry Bio-NLP</h1>
<p>A prototype API for NLP tasks in biomedical domain.</p>'''

@app.route('/bio-nlp', methods=['GET'])
def biohome():
    return '''<h1>librAIry Bio-NLP</h1>
<p>A prototype API for NLP tasks in biomedical domain:
    <ul>
      <li>Drugs</li>
    </ul>
</p>'''


# A route to return all of the available entries in our catalog.
@app.route('/bio-nlp/drugs', methods=['POST'])
def drugs():
    if not request.json or not 'text' in request.json:
        abort(400)
    drugs = p.get_drugs(request.json['text'])
    return json.dumps(drugs)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
