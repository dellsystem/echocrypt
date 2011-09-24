utils.py
	bin_from_float(num) - saining
		- given a float, turn it into a [finite] sequence of bits
		- leading 0s (but not trailing 0s) should be removed, as well as the decimal point
		- ex: 0.015 --> bin(15) 1111, 13.41 --> bin(1341) --> 10100111101

test_utils.py
	test_bin_from_float(self) - wendy
		- tests bin_from_float(num)

echonest.py
	get_random_songs(catalog=catalog, artist=artist, title=title)
	get_song_data(s) - wendy
		- given a song, get a dictionary of the following dictionaries: beats, bars, segments, sections, tatums
	

test_echonest.py
