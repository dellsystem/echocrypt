import re

def bin_from_float(num):
	str_num=str(num).replace(".", "")
	x=re.search(r"^0*(?P<lol>[0-9]*)", str_num)
	lol=x.group("lol") if x.group("lol") else "0"
	return bin(int(lol))
