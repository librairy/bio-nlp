import pysolr
import requests
import csv
from annoy import AnnoyIndex

class DrugProcessor:

    def __init__(self):
        # Setup a Solr instance. The timeout is optional.
        self.atc_solr = pysolr.Solr('http://librairy.linkeddata.es/data/atc', timeout=10)

        self.sent_solr_url = 'http://librairy.linkeddata.es/data/covid-sentences'
        self.sent_solr = pysolr.Solr(self.sent_solr_url, timeout=10)

        self.index = AnnoyIndex(186, 'angular')
        self.index.load('index.annoy')

        with open('index.dictionary', mode='r') as infile:
            reader = csv.reader(infile)
            self.index_dict = dict((rows[0],int(rows[1])) for rows in reader)

        self.index_inv_dict = {}
        for key in self.index_dict.keys():
            value = self.index_dict[key]
            self.index_inv_dict[value]=key


    def _normalize(self,drugs):
        total_frequency = sum(drugs.values())
        for key in drugs.keys():
            drugs[key] = round((drugs[key]*100)/total_frequency)
        return drugs

    def _get_drug_by_query(self,query):
        results = self.atc_solr.search(query)
        drug = {}
        for result in results:
            print(result)
            if ('label_t' in result):
                drug['name'] = result['label_t']
            if ('code_s' in result):
                drug['code'] = result['code_s']
            if ('level_i' in result):
                drug['level'] = result['level_i']
            break
        print("drug found", drug)
        return drug

    def get_drug_by_name(self, name):
        print("getting drug by name", name)
        return self._get_drug_by_query("label_t:"+name.lower())

    def get_drug_by_code(self,code):
        print("getting drug by code", code)
        return self._get_drug_by_query("code_s:"+code)


    def get_drugs(self, num):
        params = {}
        params['terms.fl']='bionlp_atc5_t'
        params['terms.sort']='count'
        params['terms.mincount']=1
        params['terms.limit']=num

        url = self.sent_solr_url + "/terms"

        resp = requests.get(url=url, params=params)
        data = resp.json()
        drugs = {}
        results = data['terms']['bionlp_atc5_t']
        i = 0
        while (i<len(results)):
            drug = results[i]
            i+=1
            frequency = results[i]
            i+=1
            drugs[drug]=frequency
        return self._normalize(drugs)


    def get_drugs_by_drug(self, code, level):
        search_word=code
        print("search-word",search_word)
        ref_index = self.index_dict[search_word]
        print("ref-index",ref_index)
        drugs = {}
        for neighbour in self.index.get_nns_by_item(ref_index, 10):
            print("neighbour",neighbour)
            neighbour_drug = self.get_drug_by_code(self.index_inv_dict[neighbour])
            drugs[neighbour_drug['code']]=neighbour_drug['name']
        return drugs
