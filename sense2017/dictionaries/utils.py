import base64
import json
import os

from fuzzywuzzy import fuzz

PROJECT_PATH = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))


def process(lexeme, examples, definition, split, data_source, num_senses, pos):
	key = encode_text('{}_senses_{}'.format(num_senses, split)).decode()

	with open(os.path.join(PROJECT_PATH, 'resources', 'pixie_dust', 'validation_map.json'), 'r') as mapping_file:
		validation_map = json.load(mapping_file)

	data = []
	with open(os.path.join(PROJECT_PATH, 'resources', 'test', validation_map[key]), 'r') as validation_file:
		header = decode_text(next(validation_file)).decode().split('\t')
		for line in validation_file:
			parts = decode_text(line).decode().split('\t')
			if (parts[0] == lexeme and parts[-1].lower() == pos.lower() and parts[-2].lower() == data_source.lower()):
				for i in range(2, len(parts)-2, 2):
					for ex in examples:
						sim1 = fuzz.ratio(parts[i].lower(), ex.lower())
						sim2 = fuzz.ratio(parts[i-1].lower(), definition.lower())
						if (sim1 > 90 or sim2 > 90):
							data.append(parts)
	return header, data


def encode_text(text, encoder=base64.b64encode):
	return encoder(text) if isinstance(text, bytes) else encoder(text.encode())


def decode_text(text, decoder=base64.b64decode):
	return decoder(text) if isinstance(text, bytes) else decoder(text.encode())