import flask
from flask import request, jsonify
from flask_cors import CORS, cross_origin
import bioprocessor
import diseaseprocessor
import drugprocessor
import articleprocessor
import json

bio_service = bioprocessor.BioProcessor()
disease_service = diseaseprocessor.DiseaseProcessor()
drug_service = drugprocessor.DrugProcessor()
article_service = articleprocessor.ArticleProcessor()

app = flask.Flask(__name__)
CORS(app)

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

def _get_drug(request):
    if (request.args.get('name')):
        return drug_service.get_drug_by_name(request.args.get('name'))
    elif (request.args.get('atc')):
        return drug_service.get_drug_by_code(request.args.get('atc'))
    else:
        print("no parameters found!!")
        return {}


@app.route('/bio-nlp/drugs', methods=['POST'])
def post_drugs():
    if not request.json or not 'text' in request.json:
        abort(400)
    drugs = bio_service.get_drugs(request.json['text'])
    return json.dumps(drugs)

@app.route('/bio-nlp/drugs', methods=['GET'])
def get_drugs():
    drugs = {}
    if (len(request.args) == 0):
        drugs = drug_service.get_drugs(10)
    else:
        print("get_drug_by_drug")
        drug = _get_drug(request)
        print("get_drug_by_drug",drug)
        if ('code' in drug):
            drugs = drug_service.get_drugs_by_drug(drug['code'],drug['level'])
    return json.dumps(drugs)


@app.route('/bio-nlp/diseases', methods=['GET'])
def get_diseases():
    diseases = {}
    if (len(request.args) == 0):
        diseases = disease_service.get_diseases(10)
    else:
        drug = _get_drug(request)
        if ('code' in drug):
            diseases = disease_service.get_diseases_by_drug(drug['code'],drug['level'])
    return json.dumps(diseases)

@app.route('/bio-nlp/articles', methods=['GET'])
def get_articles():
    articles = []
    if (len(request.args) == 0):
        articles = article_service.get_articles(10)
    else:
        drug = _get_drug(request)
        if ('code' in drug):
            articles = article_service.get_articles_by_drug(drug,10)
    return json.dumps(articles)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
