# sense2017
Task setup of the paper "[One Representation per Word - _Does it make Sense for Composition?_](http://www.aclweb.org/anthology/W17-1910)"

This package re-creates the dataset as used in the paper.

If you use this dataset in your research please use the following citation entry:

```
@InProceedings{kober-EtAl:2017:SENSE2017,
  author    = {Kober, Thomas  and  Weeds, Julie  and  Wilkie, John  and  Reffin, Jeremy  and  Weir, David},
  title     = {One Representation per Word - Does it make Sense for Composition?},
  booktitle = {Proceedings of the 1st Workshop on Sense, Concept and Entity Representations and their Applications},
  month     = {April},
  year      = {2017},
  address   = {Valencia, Spain},
  publisher = {Association for Computational Linguistics},
  pages     = {79--90},
  abstract  = {In this paper, we investigate whether an a priori disambiguation of word senses
	is strictly necessary or whether the meaning of a word in context can be
	disambiguated through composition alone. We evaluate the performance of
	off-the-shelf single-vector and multi-sense vector models on a benchmark phrase
	similarity task and a novel task for word-sense discrimination. We find that
	single-sense vector models perform as well or better than multi-sense vector
	models despite arguably less clean elementary representations. Our findings
	furthermore show that simple composition functions such as pointwise addition
	are able to recover sense specific information from a single-sense vector model
	remarkably well.},
  url       = {http://www.aclweb.org/anthology/W17-1910}
}
```

Please email the first author if you have any queries with regards to this task.

### Prerequisits

* Oxford Dictionary API Key (get from [https://developer.oxforddictionaries.com](https://developer.oxforddictionaries.com))
* Collins Dictionary API Key (get from [https://www.collinsdictionary.com/api/](https://www.collinsdictionary.com/api/))

### Installation

If the repository is cloned, the code should run without the need for running the setup files, if you want to install it anyway do the following:

	cd /path/to/sense2017
	python setup.py install
	
### Requirements

* beautifulsoup4>=4.5.1
* fuzzywuzzy>=0.15.0
* joblib>=0.9.2
* nltk>=3.0.2
* requests>=2.11.1

To install all requirements without installing `sense2017` you can run:

	cd /path/to/sense2017
	pip install -r requirements.txt

### Usage

To re-create our task run the following:

	python -m sense2017.create_dataset -oxid <OXFORD-APP-ID> -oxkey <OXFORD-APP-KEY> -cokey <COLLINS-API-KEY> -op /path/to/output/folder

