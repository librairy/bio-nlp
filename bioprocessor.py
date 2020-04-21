import spacy
import pysolr
import re

class BioProcessor:

    def __init__(self):
        # Load a SpaCy NER Model
        self.nlp = spacy.load("en_ner_bc5cdr_md")

        # Setup a Solr instance. The timeout is optional.
        self.solr = pysolr.Solr('http://librairy.linkeddata.es/solr/atc', timeout=10)

        # Setup a Solr instance. The timeout is optional.
        self.solr_diseases = pysolr.Solr('http://librairy.linkeddata.es/solr/diseases', timeout=10)

    def get_diseases(self, text):
        doc = self.nlp(text)
        candidates = []

        # Search for candidates based on SpaCy NER
        for entity in doc.ents:
            #print("----->",entity.label, entity.label_, entity.text)
            if (entity.label_ == "DISEASE" and len(entity.text) > 2):
                #print(entity.text, entity.vector_norm)
                candidates.append(entity)

        # Retrieve the ATC Code
        diseases = []
        for candidate in list(set(candidates)):
            #print("candidate: ", candidate)
            label = re.sub(r'\W+', ' ', candidate.text)
            solr_query = "name_t:\""+label+"\"^100 or synonyms:\""+label+"\"^10 or mappings:\""+label+"\"^1"
            results = self.solr_diseases.search(solr_query)
            if (len(results) == 0):
                label_tokens = label.split(" ")
                if (len(label_tokens) > 3):
                    new_label = " ".join(label_tokens[:len(label_tokens)-1])
                    solr_query = "name_t:\""+new_label+"\"^100 or synonyms:\""+new_label+"\"^10 or mappings:\""+new_label+"\"^1"
                    results = self.solr_diseases.search(solr_query)
            for result in results:
                name = result["name_t"]
                disease = {}
                disease["name"] = name
                disease['code'] =result["id"]
                disease['level']=result["level_i"]
                diseases.append(disease)
                break
        return diseases


    def get_drugs(self, text):
        doc = self.nlp(text)
        candidates = []

        # Search for candidates based on suffix
        for token in doc:
            token_text = token.text.lower()
            if ("vir" in token_text):
                candidates.append(token_text)
            elif ("feron" in token_text):
                candidates.append(token_text)
            elif ("umab" in token_text):
                candidates.append(token_text)

        # Search for candidates based on SpaCy NER
        for entity in doc.ents:
            #print("----->",entity.label, entity.label_, entity.text)
            if (entity.label_ == "CHEMICAL" and len(entity.text) > 2):
                candidates.append(entity.text.lower())

        # Retrieve the ATC Code
        drugs = []
        for candidate in list(set(candidates)):
            #print("candidate: ", candidate)
            label = re.sub(r'\W+', ' ', candidate)
            results = self.solr.search("label_t:"+label)
            for result in results:
              drug = {}
              if ("label_t" in result):
                  drug["name"] = result["label_t"]
              if ("code_s" in result):
                  drug["atc_code"] = result["code_s"]
              if ("parent_s" in result):
                  drug["atc_parent"] = result["parent_s"]
              if ("cui_s" in result):
                drug["cui"] = result["cui_s"]
              if ("level_i" in result):
                  drug["level"] = result["level_i"]
              drugs.append(drug)
              break
        return drugs
