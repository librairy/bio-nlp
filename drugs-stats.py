import pysolr

cord19_solr_url = 'http://librairy.linkeddata.es/data/covid-paragraphs'
cord19_solr = pysolr.Solr(cord19_solr_url, timeout=20)

counter = 0
completed = False
window_size=50000
cursor = "*"
drugs = {}
while (not completed):
    old_counter = counter
    try:
        query="*:*"
        fields = ["bionlp_drugs_C"+str(l)  for l in range(1,6)]
        print("searching drugs in paragraphs by: ", query , " with fields: ", fields)
        paragraphs = cord19_solr.search(q=query,fl=",".join(fields),rows=window_size,cursorMark=cursor,sort="id asc")
        cursor = paragraphs.nextCursorMark
        counter += len(paragraphs)
        for paragraph in paragraphs:
            for field in fields:
                if (field in paragraph):
                    if (not field in drugs):
                            drugs[field] = []
                    drugs[field].extend(paragraph[field])
        if (old_counter == counter):
            break
    except Exception as e:
        print(repr(e))
total = 0
for drug in drugs:
    size = len(list(set(drugs[drug])))
    print(drug,size)
    total += size
print("Total",total)
