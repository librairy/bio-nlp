import pysolr
import requests
import time

class DiseaseProcessor:

    def __init__(self):
        # Setup a Solr instance. The timeout is optional.
        self.atc_solr = pysolr.Solr('http://librairy.linkeddata.es/data/atc', timeout=10)

        self.sent_solr_url = 'http://librairy.linkeddata.es/data/covid-sentences'
        self.sent_solr = pysolr.Solr(self.sent_solr_url, timeout=10)

    def _normalize(self,diseases):
        total_frequency = sum(diseases.values())
        for key in diseases.keys():
            diseases[key] = int((diseases[key]*100)/total_frequency)
        return diseases


    def get_diseases_by_drug(self, atc_code, level):
        diseases = {}
        counter = 0
        completed = False
        window_size=100
        cursor = "*"
        while (not completed):
            old_counter = counter
            solr_query="bionlp_atc"+str(level)+"_t:"+atc_code + " AND scispacy_diseases_t:[* TO *]"
            try:
                sentences = self.sent_solr.search(q=solr_query,rows=window_size,cursorMark=cursor,sort="id asc")
                cursor = sentences.nextCursorMark
                counter += len(sentences)
                for sentence in sentences:
                  if ('scispacy_diseases_t' in sentence):
                      for disease in sentence['scispacy_diseases_t'].split(" "):
                          if (not disease in diseases):
                              diseases[disease] = 0
                          diseases[disease] += 1
                if (old_counter == counter):
                    print("done!")
                    break
            except:
                print("Solr query error. Wait for 5secs..")
                time.sleep(5.0)
        return self._normalize(diseases)

    def get_diseases(self,num):
        # http://librairy.linkeddata.es/data/covid-sentences/terms?terms.fl=scispacy_diseases_t
        params = {}
        params['terms.fl']='scispacy_diseases_t'
        params['terms.sort']='count'
        params['terms.mincount']=1
        params['terms.limit']=num

        url = self.sent_solr_url + "/terms"

        resp = requests.get(url=url, params=params)
        data = resp.json()
        diseases = {}
        results = data['terms']['scispacy_diseases_t']
        i = 0
        total_frequency = 0
        while (i<len(results)):
            disease = results[i]
            i+=1
            frequency = results[i]
            i+=1
            total_frequency += frequency
            diseases[disease]=frequency
        return self._normalize(diseases)
