import pysolr
import requests

class ParagraphProcessor:

    def __init__(self):
        self.solr = pysolr.Solr('http://librairy.linkeddata.es/data/covid-paragraphs', timeout=10)


    def get_paragraphs(self, query, size):
        results = self.solr.search(query,rows=size)
        paragraphs = []
        for result in results:
            paragraph = {}
            if ('section_s' in result):
                paragraph['section'] = result['section_s']
            if ('id' in result):
                paragraph['id'] = result['id']
            if ('text_t' in result):
                paragraph['text'] = result['text_t']
            if ('article_id_s' in result):
                paragraph['article'] = result['article_id_s']
            paragraphs.append(paragraph)
        return paragraphs
