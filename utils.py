import re
import echonest

def bin_from_float(num):
	"""
	Takes a float, strips floating point, leading zeroes, exponents and converts to binary.
	"""
	str_num = str(abs(num)).replace(".", "")
	x = re.search(r"^0*(?P<lol>[0-9]*)", str_num)
	lol = x.group("lol") if x.group("lol") else "0"
	return bin(int(lol))[2:0]
	
def generate_keystream(catalog):
	"""
	Takes a catalog id and generates four bit sequences.
	"""
	seqs=echonest.get_catalog_data(catalog)
	for seq in seqs:
		seq=[bin_from_float(x**seqs.index(seq)) for x in seq]
	streams=["".join(seq) for seq in seqs]
	
