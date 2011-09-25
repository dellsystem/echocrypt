# encoding: utf-8
import sys
import random
from lib import keystreams

def error(message):
	print message
	print "Usage: python echocrypt.py [e|d] \"message\" [keystream name]"
	exit(1)

mode = sys.argv[1]

if mode == 'e':
	# If the keystream to use is specified, use that one; otherwise, use a random one in the dictionary
	try:
		keystream_name = sys.argv[3]
	except IndexError:
		keystream_name = random.choice(keystreams.total.keys())
        print "Using keystream: %s" % keystream_name

	keystream = keystreams.total[keystream_name]
	try:
		message = sys.argv[2]
	except IndexError:
		error("You must specify a message to encrypt.")

	ciphertext = keystream.encrypt(message)
	print ciphertext

elif mode == 'd':
	try:
		message = sys.argv[2]
	except IndexError:
		error("You must specify a message to decrypt.")

	# Keystream name must be specified in this case
	try:
		keystream_name = sys.argv[3]
	except IndexError:
		error("You must specify a keystream to decrypt with.")

	keystream = keystreams.total[keystream_name]

	plaintext = keystream.decrypt(message)
	print plaintext
	

"""
if mode == 'e' or mode == 'a':
	message = sys.argv[2]
	bin_message = utils.bin_from_string(message) if mode == 'e' else message
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
elif mode == 's' or mode == 'd':
	ciphertext = sys.argv[2]
	keystream = pickle.load(open("keystream_used"))
	message = bin(int(ciphertext, 2) - int(keystream, 2))[2:]
	if mode == 's':
		num_bits = len(message) / 7
		chars = []
		for i in xrange(num_bits):
			char = chr(int(message[i*7:(i+1)*7], 2))
			chars.append(char)

		print ''.join(chars)
	else:
		print message
"""
