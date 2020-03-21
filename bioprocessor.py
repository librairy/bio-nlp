import spacy
import pysolr
import re

class BioProcessor:

    def __init__(self):
        # Load a SpaCy NER Model
        self.nlp = spacy.load("en_ner_bc5cdr_md")

        # Setup a Solr instance. The timeout is optional.
        self.solr = pysolr.Solr('http://librairy.linkeddata.es/solr/atc', timeout=10)

    def get_drugs(self, text):
        doc = self.nlp(text)
        candidates = []

        # Search for candidates based on suffix
        for token in doc:
            if (token.suffix_ == "vir"):
                candidates.append(token.text)

        # Search for candidates based on SpaCy NER
        for entity in doc.ents:
            #print("----->",entity.label, entity.label_, entity.text)
            if (entity.label_ == "CHEMICAL"):
                candidates.append(entity.text)

        # Retrieve the ATC Code
        drugs = []
        for candidate in candidates:
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
        return drugs
