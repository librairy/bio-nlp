import pysolr
import requests
import articleprocessor

class ParagraphProcessor:

    def __init__(self):
        self.solr = pysolr.Solr('http://librairy.linkeddata.es/data/covid-paragraphs', timeout=10)
        self.article_service = articleprocessor.ArticleProcessor()


    def get_paragraphs(self, query, size):
        results = self.solr.search(query,rows=size*2)
        paragraphs = []
        for result in results:
            paragraph = {}
            if ('id' in result):
                paragraph['id'] = result['id']
            if ('text_t' in result):
                paragraph['text'] = result['text_t']
            if ('article_id_s' in result):
                article_id = result['article_id_s']
                article = {}
                article['id'] = article_id
                papers = self.article_service.get_articles_by_id(article_id)
                if (len(papers) > 0):
                    paper = papers[0]
                    if ('name' in paper):
                        article['title'] = paper['name']
                    if ('section_s' in result):
                        article['section'] = result['section_s']
                    article['url'] = paper['url']
                    paragraph['article'] = article
                    paragraphs.append(paragraph)
                    if (len(paragraphs) >= size):
                        break                        
        return paragraphs
