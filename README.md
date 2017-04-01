# sense2017
Task setup of the paper "One Representation per Word - _Does it make Sense for Composition?_"

This package re-creates the dataset as used in the paper.

If you use this dataset in your research please use the following citation entry:

```
@inproceedings{Kober_2017,
	Address = {Valencia, Spain},
	Author = {Kober, Thomas and Weeds, Julie and Wilkie, John and Reffin, Jeremy and Weir, David},
	Booktitle = {Proceedings of the 1st Workshop on Sense, Concept and Entity Representations and their Applications},
	Month = {April},
	Title = {One Representation per Word --- \emph{Does it make Sense for Composition?}},
	Year = {2017}
}
```

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

