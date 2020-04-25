import flask
from flask import request, jsonify, abort
from flask_cors import CORS, cross_origin
import bioprocessor
import diseaseprocessor
import drugprocessor
import articleprocessor
import paragraphprocessor
import json

bio_service = bioprocessor.BioProcessor()
disease_service = diseaseprocessor.DiseaseProcessor()
drug_service = drugprocessor.DrugProcessor()
article_service = articleprocessor.ArticleProcessor()
paragraph_service = paragraphprocessor.ParagraphProcessor()

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


def _get_drugs(request):
    drugs = []
    if (request.args.get('keywords')):
        keywords = request.args.get('keywords')
        for keyword in keywords.split("+"):
            drugs.append(drug_service.get_drug_by_keyword(keyword))
    return drugs


##################################################################################################
######
######          Bio NLP
######
##################################################################################################


@app.route('/bio-nlp/drugs', methods=['POST'])
def post_drugs():
    if not request.json or not 'text' in request.json:
        abort(400)
    drugs = bio_service.get_drugs(request.json['text'])
    return jsonify(drugs)

@app.route('/bio-nlp/diseases', methods=['POST'])
def post_diseases():
    if not request.json or not 'text' in request.json:
        abort(400)
    diseases = bio_service.get_diseases(request.json['text'])
    return jsonify(diseases)


##################################################################################################
######
######          Bio API
######
##################################################################################################

def get_query_param(request):
    keywords = ""
    if ('keywords' in request.args):
        keywords = request.args['keywords']

    drugs_filter = []
    diseases_filter = []
    text_filter = []

    for keyword in keywords.split(","):
        if (keyword == ""):
            print("no params")
            break

        for kw_as_drug in  drug_service.find_drugs(keyword):
            drugs_filter.append("bionlp_drugs_C"+str(kw_as_drug['level'])+":"+kw_as_drug['code'])
            break

        for kw_as_disease in  disease_service.find_diseases(keyword):
            diseases_filter.append("bionlp_diseases_C"+str(kw_as_disease['level'])+":"+kw_as_disease['code'])
            break

        text_filter.append("text_t:\""+keyword+"\"")

    query_filter = []
    if (len(drugs_filter) > 0 ):
        query_filter.append("(" + " AND ".join(drugs_filter) + ")")
    if (len(diseases_filter) > 0 ):
        query_filter.append("(" + " AND ".join(diseases_filter)  + ")")
    if (len(text_filter) > 0 ):
        query_filter.append("(" + " AND ".join(text_filter)  + ")")
    query = "*:*"
    if (len(query_filter) >0 ):
        query = " OR ".join(query_filter)
    return query

def get_size_param(request):
    size = 10
    if ('size' in request.args):
        size = request.args['size']
    return int(size)

def get_level_param(request):
    level=-1
    if ('level' in request.args):
        level = request.args['level']
    return int(level)


@app.route('/bio-api/drugs', methods=['GET'])
def get_drugs():
    size = get_size_param(request)
    level= get_level_param(request)
    query = get_query_param(request)
    drugs = drug_service.get_drugs(query,size,level)
    return jsonify(drugs)


@app.route('/bio-api/diseases', methods=['GET'])
def get_diseases():
    size = get_size_param(request)
    level= get_level_param(request)
    query = get_query_param(request)
    diseases = disease_service.get_diseases(query,size,level)
    return jsonify(diseases)

@app.route('/bio-api/articles', methods=['GET'])
def get_articles():
    articles = []
    if (len(request.args) == 0):
        articles = article_service.get_articles(10)
    else:
        for keyword in request.args.get('keywords').split(","):

            for drug in drug_service.get_drugs_by_keyword(keyword):
                articles.extend(article_service.get_articles_by_drug(drug['code'],10))

            for disease in disease_service.get_diseases_by_keyword(keyword):
                articles.extend(article_service.get_articles_by_disease(disease['name'],10))

            articles.extend(article_service.get_articles_by_keyword(keyword,10))

    return jsonify(articles)

@app.route('/bio-api/paragraphs', methods=['GET'])
def get_paragraphs():
    size = get_size_param(request)
    query = get_query_param(request)
    paragraphs = paragraph_service.get_paragraphs(query,size)
    return jsonify(paragraphs)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
