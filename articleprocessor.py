import pysolr
import requests

class ArticleProcessor:

    def __init__(self):
        self.art_solr = pysolr.Solr('http://librairy.linkeddata.es/data/covid', timeout=10)

    def _get_articles_by_query(self,query,num):
        results = self.art_solr.search(query,rows=num)
        articles = []
        for result in results:
            article = {}
            if ('name_s' in result):
                article['name'] = result['name_s']
            if ('id' in result):
                article['id'] = result['id']
            if ('abstract_t' in result):
                article['abstract'] = result['abstract_t']
            if ('url_s' in result):
                article['url'] = result['url_s']
            articles.append(article)
        return articles



    def get_articles(self, num):
        return self._get_articles_by_query("*:*",num)

    def get_articles_by_disease(self, keyword, num):
        return self._get_articles_by_query("scispacy_diseases_t:"+keyword,num)

    def get_articles_by_drug(self, keyword, num):
        query = " or ".join(["labels"+str(i)+"_t:"+keyword for i in range(1,6)])
        print(query)
        return self._get_articles_by_query(query,num)

    def get_articles_by_keyword(self, keyword, num):
        return self._get_articles_by_query("id:"+keyword + " or name_s:\""+keyword+"\" or abstract_t:\""+keyword + "\" or txt_t:\""+keyword+"\"",num)

    def get_articles_by_id(self, keyword, num=1):
        return self._get_articles_by_query("id:"+keyword,num)

    def get_articles_by_name(self, keyword, num):
        return self._get_articles_by_query("name_s:\""+keyword+"\"",num)

    def get_articles_by_abstract(self, keyword, num):
        return self._get_articles_by_query("abstract_t:\""+keyword+"\"",num)

    def get_articles_by_text(self, keyword, num):
        return self._get_articles_by_query("txt_t:\""+keyword+"\"",num)
