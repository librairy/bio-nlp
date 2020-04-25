import pysolr
import requests
import csv
from annoy import AnnoyIndex

class DrugProcessor:

    def __init__(self):
        # Setup a Solr instance. The timeout is optional.
        self.atc_solr = pysolr.Solr('http://librairy.linkeddata.es/data/atc', timeout=20)

        self.cord19_solr_url = 'http://librairy.linkeddata.es/data/covid-paragraphs'
        self.cord19_solr = pysolr.Solr(self.cord19_solr_url, timeout=20)

        self.index = AnnoyIndex(186, 'angular')
        self.index.load('index.annoy')

        with open('index.dictionary', mode='r') as infile:
            reader = csv.reader(infile)
            self.index_dict = dict((rows[0],int(rows[1])) for rows in reader)

        self.index_inv_dict = {}
        for key in self.index_dict.keys():
            value = self.index_dict[key]
            self.index_inv_dict[value]=key


    def find_drugs(self, keyword):
        query = "label_t:\""+keyword+"\" or code_s:"+keyword + " or id:" + keyword
        results = self.atc_solr.search(query)
        drugs= []
        for result in results:
            drug = {}
            if ('label_t' in result):
                drug['name'] = result['label_t']
            if ('id' in result):
                drug['code'] = result['id']
            if ('level_i' in result):
                drug['level'] = result['level_i']
            drugs.append(drug)
        print("found drugs",drugs)
        return drugs

    def get_drugs_as_terms(self, size,level):
        params = {}
        drug_level = 5
        if (int(level) > 0):
            drug_level=level
        field = 'bionlp_drugs_C'+str(drug_level)
        params['terms.fl']=field
        params['terms.sort']='count'
        params['terms.mincount']=1
        params['terms.limit']=size

        url = self.cord19_solr_url + "/terms"
        resp = requests.get(url=url, params=params)
        data = resp.json()
        print(data)
        drugs = []
        results = data['terms'][field]
        i = 0
        while (i<len(results)):
            drug_code = results[i]
            print("drug code", drug_code)
            i+=1
            frequency = results[i]
            i+=1
            drugs_candidates = self.find_drugs(drug_code.upper())
            if (len(drugs_candidates) >0 ):
                drug = drugs_candidates[0]
                drug['freq'] = frequency
                drugs.append(drug)
        return drugs


    def get_drugs(self, query, size, level):
        if (query == "*:*"):
            return self.get_drugs_as_terms(size,level)
        counter = 0
        completed = False
        window_size=50000
        cursor = "*"
        drugs = {}
        while (not completed):
            old_counter = counter
            try:
                fields = ["bionlp_drugs_N"+str(l)  for l in range(1,6)]
                if (int(level) >= 0):
                    fields = ["bionlp_drugs_N"+str(level)]
                print("searching drugs in paragraphs by: ", query , " with fields: ", fields)
                paragraphs = self.cord19_solr.search(q=query,fl=",".join(fields),rows=window_size,cursorMark=cursor,sort="id asc")
                cursor = paragraphs.nextCursorMark
                counter += len(paragraphs)
                for paragraph in paragraphs:
                    for field in fields:
                        if (field in paragraph):
                            for drug in paragraph[field]:
                                if (not drug in drugs):
                                    drugs[drug] = 0
                                drugs[drug] = drugs[drug] +1
                if (old_counter == counter):
                    break
            except Exception as e:
                print(repr(e))
        result = []
        for w in sorted(drugs, key=drugs.get, reverse=True):
            found_drugs = self.find_drugs(w)
            if (len(found_drugs) > 0):
                drug = found_drugs[0]
                drug['freq'] = drugs[w]
                result.append(drug)
            if (len(result) >= size):
                break
        return result

    def get_related_drugs(self, code, level):
        search_word=code
        #print("search-word",search_word)
        ref_index = self.index_dict[search_word]
        #print("ref-index",ref_index)
        drugs = {}
        for neighbour in self.index.get_nns_by_item(ref_index, 11):
            #print("neighbour",neighbour)
            neighbour_code=self.index_inv_dict[neighbour]
            if (code != neighbour_code):
                neighbour_drug = self.get_drug_by_code(neighbour_code)
                drugs[neighbour_drug['code']]=neighbour_drug['name']
        return drugs
