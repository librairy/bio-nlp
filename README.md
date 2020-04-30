# Basic Overview

Natural Language Processing tasks focused on Biological domain available from a RESTful API:
* `/drugs` : retrieves the drugs in a text, along with their Anatomical Therapeutic Chemical Classification (ATC) code

# Web Page
Available at: [https://librairy.github.io/bio-nlp/](https://librairy.github.io/bio-nlp/)

# Natural Language Processing API
Available at: [http://librairy.linkeddata.es/bio-nlp](http://librairy.linkeddata.es/bio-nlp)

This is an example of a CURL query:
```sh
curl -d '{"text":"however, clinical trials investigating the efficacy of several agents, including remdesivir and chloroquine, are underway in China"}' -H "Content-Type: application/json" -X POST https://librairy.linkeddata.es/bio-nlp/drugs
```

And the answer is:
```json
[{
	"name": "remdesivir",
	"atc_parent": "J05AB"
}, {
	"name": "chloroquine",
	"atc_code": "P01BA01",
	"atc_parent": "P01BA",
	"cui": "C0008269",
	"level": 5
}]
```

# Biomedical Literature API
Available at: [http://librairy.linkeddata.es/bio-api](http://librairy.linkeddata.es/bio-api)

Some examples:
## Most frequent drugs..
* ..used in the experiments: [https://librairy.linkeddata.es/bio-api/drugs](https://librairy.linkeddata.es/bio-api/drugs)
* ..grouped by therapeutic group (ATC-4): [https://librairy.linkeddata.es/bio-api/drugs?level=4](https://librairy.linkeddata.es/bio-api/drugs?level=4)
* ..considered together with *lopinavir*: [https://librairy.linkeddata.es/bio-api/drugs?keywords=lopinavir](https://librairy.linkeddata.es/bio-api/drugs?keywords=lopinavir)
* ..used as *viral vaccines*: [https://librairy.linkeddata.es/bio-api/drugs?keywords=viral%20vaccines&level=5](https://librairy.linkeddata.es/bio-api/drugs?keywords=viral%20vaccines&level=5)
* ..used to handle *fever*: [https://librairy.linkeddata.es/bio-api/drugs?keywords=fever&level=5](https://librairy.linkeddata.es/bio-api/drugs?keywords=fever&level=5)

## Most frequent diseases..
* ..considered in the corpus: [https://librairy.linkeddata.es/bio-api/diseases](https://librairy.linkeddata.es/bio-api/diseases)
* ..grouped by symptoms : [https://librairy.linkeddata.es/bio-api/diseases?level=2](https://librairy.linkeddata.es/bio-api/diseases?level=2)
* .. treated by *chloroquine*: [https://librairy.linkeddata.es/bio-api/diseases?keywords=chloroquine](https://librairy.linkeddata.es/bio-api/diseases?keywords=chloroquine)
* ..appearing along with *hallucination*: [https://librairy.linkeddata.es/bio-api/diseases?keywords=hallucination](https://librairy.linkeddata.es/bio-api/diseases?keywords=hallucination)

## Texts about...
* About covid-19 and inflammation difficulties: [https://librairy.linkeddata.es/bio-api/texts?keywords=covid19,inflammation](https://librairy.linkeddata.es/bio-api/texts?keywords=covid19,inflammation)
* About *hydroxychloroquine*: [https://librairy.linkeddata.es/bio-api/texts?keywordshydroxychloroquine](https://librairy.linkeddata.es/bio-api/texts?keywordshydroxychloroquine)
