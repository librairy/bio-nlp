# Basic Overview

Natural Language Processing tasks focused on Biological domain available from a RESTful API:
* `/drugs` : retrieves the drugs in a text, along with their Anatomical Therapeutic Chemical Classification (ATC) code

# Web Page
Available at: [https://librairy.github.io/bio-nlp/](https://librairy.github.io/bio-nlp/)

# RESTFul API
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
