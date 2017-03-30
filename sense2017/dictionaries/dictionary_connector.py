import logging

from bs4 import BeautifulSoup
from fuzzywuzzy import fuzz
from nltk.corpus import semcor
from nltk.corpus.reader.wordnet import Lemma
from nltk.corpus.reader.wordnet import Synset
from nltk.corpus import wordnet
import requests


class OxfordAPIConnector:
	def __init__(self, app_id, app_key, **kwargs):
		self._base_url = kwargs.get('base_url', 'https://od-api.oxforddictionaries.com/api/v1')
		self._headers = {'app_key': app_key, 'app_id': app_id}
		self._processor = kwargs.get('processor', lambda lexeme, definition, examples: (lexeme, definition, examples))

	def request_data_for_lexeme(self, lexeme, target_def, api_endpoint='/entries/en/'):
		req_url = '{}{}{}'.format(self._base_url, api_endpoint, lexeme)
		logging.info('Requesting data from {}...'.format(req_url))

		r = requests.get('{}'.format(req_url), headers=self._headers)

		if (r.ok):
			definition = ''
			examples = []
			max_sim = 0

			for entry in r.json()['results']:
				for lex_entry in entry.get('lexicalEntries', []):
					for eentry in lex_entry.get('entries', []):
						for sense in eentry.get('senses', []):
							for sense_def in sense.get('definitions', []):
								sim = fuzz.ratio(sense_def.lower(), target_def.lower())
								if (sim >= 90 and sim > max_sim): # Allow a bit of slack (punctuation and stuff)
									max_sim = sim
									definition = sense_def.lower()
									examples = []
									for ex in sense.get('examples', []):
										examples.append(ex['text'])
							if ('subsenses' in sense):
								for subsense in sense.get('subsenses', []):
									for subsense_def in subsense.get('definitions', []):
										sim = fuzz.ratio(subsense_def.lower(), target_def.lower())
										if (sim >= 90 and sim > max_sim):  # Allow a bit of slack (punctuation and stuff)
											max_sim = sim
											definition = subsense_def.lower()
											examples = []
											for ex in subsense.get('examples', []):
												examples.append(ex['text'])

			return self._processor(lexeme=lexeme, definition=definition, examples=examples)
		else:
			logging.error('Request to {} failed with status code={}! Reason={}!\nResponse={}'.format(req_url, r.status_code,
																									 r.reason, r.text))
			return None


class CollinsAPIConnector:
	def __init__(self, api_key, **kwargs):
		self._base_url = kwargs.get('base_url', 'https://api.collinsdictionary.com/api/v1/dictionaries')
		self._headers = {'Accept': 'application/json', 'accessKey': api_key}
		self._processor = kwargs.get('processor', lambda lexeme, definition, examples: (lexeme, definition, examples))

	def request_entry_ids_for_lexeme(self, lexeme, api_endpoint='/english-learner/search/'):
		req_url = '{}{}?q={}&pagesize=20&pageindex=1'.format(self._base_url, api_endpoint, lexeme)
		r = requests.get('{}'.format(req_url), headers=self._headers)
		entry_ids = []

		for entry in r.json()['results']:
			entry_ids.append(entry['entryId'])

		return entry_ids

	def request_data_for_lexeme(self, lexeme, target_def, api_endpoint='/english-learner/entries/'):

		entry_ids = self.request_entry_ids_for_lexeme(lexeme=lexeme)
		logging.info('Found {} entry ids for lexeme={}!'.format(len(entry_ids), lexeme))

		for entry_id in entry_ids:
			req_url = '{}{}{}?format=html'.format(self._base_url, api_endpoint, entry_id)
			logging.info('Requesting data from {}...'.format(req_url))

			r = requests.get('{}'.format(req_url), headers=self._headers)

			if (r.ok):
				soup = BeautifulSoup(r.json()['entryContent'], 'html.parser')

				definition = ''
				examples = []

				for hom in soup.find_all('div', {'class': 'hom'}):
					#for pos in hom.find_all('span', {'class': 'pos'}):
					#	print(pos.text)
					for sense in hom.find_all('div', {'class': 'sense'}):
						sense_def = sense.find('span', {'class': 'def'})

						if (fuzz.ratio(target_def.lower(), sense_def.text.lower()) >= 90):
							definition = sense_def.text

							for cit in sense.find_all('span', {'class': 'cit'}):
								for example in cit.find_all('span', {'class': 'quote'}):
									examples.append(example.text)
							break

					if (definition is not None and definition != ''): break

				return self._processor(lexeme=lexeme, definition=definition, examples=examples)
			else:
				logging.error('Request to {} failed with status code={}! Reason={}!\nResponse={}'.format(req_url, r.status_code,
																										 r.reason, r.text))
				return None


class SemCorAPIConnector:
	def __init__(self, **kwargs):

		self._sents = []
		self._tagged_sents = []
		self._semcor_file_ids = self._load_semcor_file_ids()
		self._processor = kwargs.get('processor', lambda lexeme, definition, examples: (lexeme, definition, examples))

		for file_id in self._semcor_file_ids:
			self._sents.append(semcor.sents(file_id))
			self._tagged_sents.append(semcor.tagged_sents(file_id, 'both'))

	def find_data_for_synset(self, synset, lexeme):
		synset = synset if isinstance(synset, Synset) else wordnet.synset(synset)

		definition = ''
		examples = []

		for idx, (sent_chunks, tagged_sent_chunks) in enumerate(zip(self._sents, self._tagged_sents), 1):
			if (idx % 50 == 0): logging.info('\tProcessed {}/{} chunks!'.format(idx, len(self._sents)))
			for sent_chunk, tagged_sent_chunk in zip(sent_chunks, tagged_sent_chunks):
				for tree in tagged_sent_chunk:
					if (isinstance(tree.label(), Lemma) and tree.label().synset() == synset):
						definition = synset.name()
						examples.append(' '.join(sent_chunk))
						break

		return self._processor(lexeme=lexeme, definition=definition, examples=examples)

	def _load_semcor_file_ids(self):
		try:
			semcor_file_ids = semcor.fileids()
		except LookupError as le:
			import nltk
			logging.warning(le)
			logging.info('Downloading SemCor corpus...')
			status = nltk.download('semcor')
			if (status):
				logging.info('SemCor downloaded successfully!')
				semcor_file_ids = semcor.fileids()
			else:
				logging.error('Downloading SemCor failed!')
				raise LookupError(le)
		return semcor_file_ids
