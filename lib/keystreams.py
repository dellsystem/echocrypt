import utils
import echonest
import cPickle as pickle

filename = "data/keystreams" # for storing total

# Re-pickles the total dictionary
def repickle():
	file = open(filename, "wb")
	pickle.dump(total, file)
	file.close()

class Keystream:
	def __init__(self, name):
		self.name = name
		# Add it to the dictionary containing all the keystreams
		total[name] = self

		# Get some random tracks from the specified catalog
		self.tracks = echonest.get_catalog_tracks()
		tracks_data = [echonest.get_track_data(track) for track in self.tracks]
		# This should be fixed - don't save the raw track data, just save the track names etc
		self.bitstream = '0'.join(['0'.join(x) for x in utils.do_something_weird(tracks_data)])
		self.encrypt_pointer = 0
		self.decrypt_pointer = 0
		repickle()

	def encrypt(self, message):
		bin_message = utils.bin_from_string(message)
		num_chars = len(bin_message)
		keystream_used = self.bitstream[self.encrypt_pointer:self.encrypt_pointer+num_chars]
		# Move the pointer to the end of the used keystream
		self.encrypt_pointer += num_chars
		repickle()
		ciphertext = bin(int(bin_message, 2) + int(keystream_used, 2))[2:] # hahahahhaha
		return ciphertext

	def decrypt(self, ciphertext):
		"""
		print self.encrypt_pointer
		print len(ciphertext)
		num_chars = self.encrypt_pointer  # or not, check it out
		"""
		try:
			keystream_used = self.bitstream[self.decrypt_pointer:self.decrypt_pointer+len(ciphertext)-1]
			message = bin(int(ciphertext, 2) - int(keystream_used, 2))[2:]
			self.decrypt_pointer += len(ciphertext) - 1 # lol
		except ValueError: # I'M NOT SURE IF THIS IS NECESSARY BUT JUST IN CASE
			keystream_used = self.bitstream[self.decrypt_pointer:self.decrypt_pointer+len(ciphertext)-2]
			message = bin(int(ciphertext, 2) - int(keystream_used, 2))[2:]
			self.decrypt_pointer += len(ciphertext) - 2 # lol
		num_bits = len(message) / 7
		chars = []
		for i in xrange(num_bits):
			char = chr(int(message[i*7:(i+1)*7], 2))
			chars.append(char)

		return ''.join(chars)
		repickle()

	# Returns the number of characters left for decrypting (not encrypting)
	def get_chars_left(self):
		return len(self.bitstream) - self.encrypt_pointer

	def delete(self):
		del total[self.name]
		repickle()

	def reset(self):
		self.encrypt_pointer = 0
		self.decrypt_pointer = 0

try:
	file = open(filename, 'rb')
	total = pickle.load(file)
except IOError:
	total = {}
