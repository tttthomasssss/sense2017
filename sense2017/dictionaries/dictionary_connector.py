import logging

from fuzzywuzzy import fuzz
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
				for lex_entry in entry['lexicalEntries']:
					for eentry in lex_entry['entries']:
						for sense in eentry['senses']:
							for sense_def in sense['definitions']:
								sim = fuzz.ratio(sense_def.lower(), target_def.lower())
								if (sim >= 90 and sim > max_sim): # Allow a bit of slack (punctuation and stuff)
									max_sim = sim
									definition = sense_def.lower()
									examples = []
									for ex in sense['examples']:
										examples.append(ex['text'])
							if ('subsenses' in sense):
								for subsense in sense['subsenses']:
									for subsense_def in subsense['definitions']:
										sim = fuzz.ratio(subsense_def.lower(), target_def.lower())
										if (sim >= 90 and sim > max_sim):  # Allow a bit of slack (punctuation and stuff)
											max_sim = sim
											definition = subsense_def.lower()
											examples = []
											for ex in subsense['examples']:
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
			req_url = '{}{}{}?format=xml'.format(self._base_url, api_endpoint, entry_id)
			logging.info('Requesting data from {}...'.format(req_url))

			r = requests.get('{}'.format(req_url), headers=self._headers)

			if (r.ok):
				print('XXX: {}'.format(r.json()['entryContent']))
			else:
				logging.error('Request to {} failed with status code={}! Reason={}!\nResponse={}'.format(req_url, r.status_code,
																										 r.reason, r.text))

class SemCorAPIConnector:
	def __init__(self):
		pass