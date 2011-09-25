# encoding: utf-8
import sys
import cPickle as pickle
import utils

mode = sys.argv[1]

if mode == 'e':
	message = sys.argv[2]
	bin_message = utils.bin_from_string(message)
	num_chars = len(bin_message)

	total_keystream = pickle.load(open("keystreams"))
	keystream = total_keystream[:num_chars]
	print bin_message
	print "---------"
	print keystream
	# Save it to a file
	pickle.dump(keystream, open("keystream_used", "wb"))

	print "---------"

	ciphertext = bin(int(bin_message, 2) + int(keystream, 2))[2:]
	print ciphertext
elif mode == 'd':
	ciphertext = sys.argv[2]
	keystream = pickle.load(open("keystream_used"))
	message = bin(int(ciphertext, 2) - int(keystream, 2))[2:]
	num_bits = len(message) / 7
	chars = []
	for i in xrange(num_bits):
		char = chr(int(message[i*7:(i+1)*7], 2))
		chars.append(char)

	print ''.join(chars)