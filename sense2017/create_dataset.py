from argparse import ArgumentParser
from functools import partial
from time import sleep
import logging
import os
import sys

from sense2017.dictionaries.dictionary_connector import OxfordAPIConnector
from sense2017.dictionaries.dictionary_connector import CollinsAPIConnector
from sense2017.dictionaries import utils

parser = ArgumentParser()
parser.add_argument('-oxid', '--oxford-dictionary-app-id', type=str, required=True, help='Oxford Dictionaries App ID')
parser.add_argument('-oxkey', '--oxford-dictionary-app-key', type=str, required=True, help='Oxford Dictionaries App Key')
parser.add_argument('-co', '--collins-dictionary-api-key', type=str, required=True, help='Collins Dictionary API Key')
parser.add_argument('-op', '--output-path', type=str, required=True, help='Output Path')
parser.add_argument('-o', '--output-file', type=str, default='sense2017_WSD.txt', help='Output File name')
parser.add_argument('-v', '--validate', action='store_true', help='Validate dataset')
parser.add_argument('-to', '--timeout', type=int, default=5, help='Timeout between requests')
parser.add_argument('-ns', '--num-senses', type=int, default=-1, help='Number of senses for task (2-5; pass -1 for all)')
parser.add_argument('-pos', '--part-of-speech', type=str, default='all', help='Part of speech for task ([adjective|noun|verb|all])')


def create_dataset(num_senses, pos, split, timeout, ox_app_id, ox_app_key):
	header = 'Lexeme\tTarget Sense Definition\tTarget Sense Sentence'
	for i in range(1, num_senses+1):
		header += '\tExample Definition Sense {}\tExample Sentence Sense {}'.format(i, i)
	header += '\tData Source\tPoS'
	dataset = [header.split('\t')]

	# Process Oxford
	'''
	logging.info('Loading data from Oxford Dictionary...')
	ox_processor = partial(utils.process_oxford, data_source='oxford', num_senses=num_senses, pos=pos, split=split)
	ox = OxfordAPIConnector(app_id=ox_app_id, app_key=ox_app_key, processor=ox_processor)

	with open(os.path.join(utils.PROJECT_PATH, 'resources', 'definitions', '{}_senses'.format(num_senses), split,
						   'oxford', 'sense2017_wsd_task.txt'), 'r') as in_file:
		next(in_file) # Skip Header
		for idx, line in enumerate(in_file):
			parts = line.strip().split('\t')
			if (parts[-1].lower() == pos.lower()):
				_, data_point = ox.request_data_for_lexeme(lexeme=parts[0], target_def=parts[1])
				dataset.append(data_point)
				sleep(timeout)
	'''
	# Process Collins
	logging.info('Loading data from Collins Dictionary...')
	co = CollinsAPIConnector(api_key='iGv4TgxWSxWhD7w2RZv5CB2GZDTtcmd9uxdSY1VNnvZOXZxmBjinibCGx63Fjk09')
	co.request_data_for_lexeme('take', 'geh in oasch')




if (__name__ == '__main__'):
	args = parser.parse_args()

	log_formatter = logging.Formatter(fmt='%(asctime)s: %(levelname)s - %(message)s', datefmt='[%d/%m/%Y %H:%M:%S %p]')
	root_logger = logging.getLogger()
	root_logger.setLevel(logging.DEBUG)

	console_handler = logging.StreamHandler(sys.stdout)
	console_handler.setFormatter(log_formatter)
	root_logger.addHandler(console_handler)

	base_url = 'https://od-api.oxforddictionaries.com/api/v1'
	app_id = '5119d99d'
	app_key = '7a4eaa5a7dd12b30a8171c39b31aa760'
	headers = {'app_id': app_id, 'app_key': app_key}

	collins_1 = 'iGv4TgxWSxWhD7w2RZv5CB2GZDTtcmd9uxdSY1VNnvZOXZxmBjinibCGx63Fjk09'
	collins_2 = 'Eqno7D19D1BRrMfZK4DTLw4sGmGt8ylx5WhEZDTPRzQDhEnKJpdt2gcIM4At3pdu'

	if (args.num_senses <= 0):
		num_senses = range(2, 6)
	else:
		num_senses = [args.num_senses]

	if (args.part_of_speech.lower() == 'all'):
		posse = ['Adjective', 'Noun', 'Verb']
	else:
		posse = [args.part_of_speech]

	for split in ['dev', 'test']:
		for ns in num_senses:
			for pos in posse:
				create_dataset(num_senses=ns, pos=pos, split=split, timeout=args.timeout, ox_app_id=app_id,
							   ox_app_key=app_key)


