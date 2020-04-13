import pysolr
import requests

class ArticleProcessor:

    def __init__(self):
        # Setup a Solr instance. The timeout is optional.
        self.art_solr = pysolr.Solr('http://librairy.linkeddata.es/data/covid', timeout=10)

    def get_articles(self, num):
        query = "*:*"
        results = self.art_solr.search(query,rows=num)
        articles = []
        for result in results:
            article = {}
            if ('name_s' in result):
                article['name'] = result['name_s']
            if ('id' in result):
                article['id'] = result['id']
            if ('url_s' in result):
                article['url'] = result['url_s']
            articles.append(article)
        return articles


    def get_articles_by_drug(self, drug, num):
        query = "labels"+str(drug['level'])+"_t:"+drug['code']
        results = self.art_solr.search(query,rows=num)
        articles = []
        for result in results:
            article = {}
            if ('name_s' in result):
                article['name'] = result['name_s']
            if ('id' in result):
                article['id'] = result['id']
            if ('url_s' in result):
                article['url'] = result['url_s']
            articles.append(article)
        return articles
