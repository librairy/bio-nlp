import pysolr
import requests
import csv
from annoy import AnnoyIndex

class DiseaseProcessor:

    def __init__(self):
        # Setup a Solr instance. The timeout is optional.
        self.diseases_solr = pysolr.Solr('http://librairy.linkeddata.es/data/diseases', timeout=20)

        self.cord19_solr_url = 'http://librairy.linkeddata.es/data/covid-paragraphs'
        self.cord19_solr = pysolr.Solr(self.cord19_solr_url, timeout=20)


    def find_diseases(self, keyword):
        query = "name_t:\""+keyword+"\" or synonyms:\""+keyword + "\" or mappings:\""+ keyword + "\" or id:" + keyword
        results = self.diseases_solr.search(query)
        diseases= []
        for result in results:
            disease = {}
            if ('name_t' in result):
                disease['name'] = result['name_t']
            if ('id' in result):
                disease['code'] = result['id']
            if ('level_i' in result):
                disease['level'] = result['level_i']
            diseases.append(disease)
        #print("found diseases",diseases)
        return diseases

    def get_diseases_as_terms(self, size,level):
        params = {}
        disease_level = 5
        if (int(level) > 0):
            disease_level=level
        field = 'bionlp_diseases_C'+str(disease_level)
        params['terms.fl']=field
        params['terms.sort']='count'
        params['terms.mincount']=1
        params['terms.limit']=size

        url = self.cord19_solr_url + "/terms"
        resp = requests.get(url=url, params=params)
        data = resp.json()
        #print(data)
        diseases = []
        results = data['terms'][field]
        i = 0
        while (i<len(results)):
            disease_code = results[i]
            #print("disease code", disease_code)
            i+=1
            frequency = results[i]
            i+=1
            diseases_candidates = self.find_diseases(disease_code.upper())
            if (len(diseases_candidates) >0 ):
                disease = diseases_candidates[0]
                disease['freq'] = frequency
                diseases.append(disease)
        return diseases


    def get_diseases(self, query, size, level):
        if (query == "*:*"):
            return self.get_diseases_as_terms(size,level)
        counter = 0
        completed = False
        window_size=50000
        cursor = "*"
        diseases = {}
        while (not completed):
            old_counter = counter
            try:
                fields = ["bionlp_diseases_N"+str(l)  for l in range(1,20)]
                if (int(level) >= 0):
                    fields = ["bionlp_diseases_N"+str(level)]
                #print("searching diseases in paragraphs by: ", query , " with fields: ", fields)
                paragraphs = self.cord19_solr.search(q=query,fl=",".join(fields),rows=window_size,cursorMark=cursor,sort="id asc")
                cursor = paragraphs.nextCursorMark
                counter += len(paragraphs)
                for paragraph in paragraphs:
                    for field in fields:
                        if (field in paragraph):
                            for disease in paragraph[field]:
                                if (not disease in diseases):
                                    diseases[disease] = 0
                                diseases[disease] = diseases[disease] +1
                if (old_counter == counter):
                    break
            except Exception as e:
                print(repr(e))
        result = []
        for w in sorted(diseases, key=diseases.get, reverse=True):
            found_diseases = self.find_diseases(w)
            if (len(found_diseases) > 0):
                disease = found_diseases[0]
                disease['freq'] = diseases[w]
                result.append(disease)
            if (len(result) >= size):
                break
        return result
