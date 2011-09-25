import re
import echonest

def bin_from_float(num):
	"""
	Takes a float, strips floating point, leading zeroes, exponents and converts to binary.
	"""
	str_num = str(abs(num)).replace(".", "")
	x = re.search(r"^0*(?P<lol>[0-9]*)", str_num)
	lol = x.group("lol") if x.group("lol") else "0"
	return bin(int(lol))[2:]

def do_something_weird(tracks_data):
	print "in do_something_weird"
	to_return = []
	for i in xrange(4):
		this_zip = zip(tracks_data[0][i], tracks_data[1][i], tracks_data[2][i], tracks_data[3][i])
		this_list = [bin_from_float(x[0] + 2*x[1] + 3*x[2] + 4*x[3]) for x in this_zip]
		to_return.append(this_list)
	return to_return


def bin_from_string(s):
	chars = []
	for c in s:
		chars.append(bin(ord(c))[2:].zfill(7))
	return ''.join(chars)
