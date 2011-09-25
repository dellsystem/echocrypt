manage.py
	* setup
		- Interactive prompt
		- First, obtain an API key and enter it (or use the default one lol), will save in settings.yaml
		- Either give it a directory containing your MP3s, or ignore and just use a default catalog
		- If you choose to give it a directory, it will run personal_catalog_scanner.py, create a catalog with your music, and upload it, then save that catalog ID in settings.yaml
		- Then, will add a playlist containing 5 random songs from http://developer.echonest.com/api/v4/playlist/static?api_key=N6E4NIOVYMTHNDM8J&seed_catalog=CAFAHCC1329DCB5C35&format=json&results=5&type=catalog-radio&adventurousness=0.8&variety=0.8 (settings can be toggled etc)
	* add
		- add a playlist
	* delete
		- delete a playlist
	* info
		- tells you about your playlists
echocrypt.py
	* encrypt
		- pass it a message (args[1]) and it will output that message plus a random keystream to stdout
	* decrypt
		- pass it a message (args[1]) and it will output that message minus the relevant keystream (indicated by the first couple of bytes) to stdout
lib/
	utils.py
		* bin_from_float(num):
			- given a float, turn it into a [finite] sequence of bits
		* generate_keystreams(catalog):
			- add together all the strings, return 4 combined "bit sequences"
	echonest.py
		* get_catalog_tracks(catalog):
			- give it a catalog ID, will get 4 songs from that catalog
		* get_track_data(track):
			- will return: a list of lists of floats
	personal_catalog_scanner.py
	settings.py
	temp_db.py
		* keystreams, dict:
			id: keystream, etc
tests/
	test_utils.py
		* test_bin_from_float(self):
			- leading 0s (but not trailing 0s) should be removed, as well as the decimal point
			- ex: 0.015 --> bin(15) 1111, 13.41 --> bin(1341) --> 10100111101
			- 0.0 --> 0
	test_echonest.py
data/
	settings.yaml
		* api_key
		* catalog_id
	db.sqlite
		* keystreams
			* id (int) - each playlist generates 4 keystreams but it doesn't matter which playlist a keystream is from
			* keystream (binary?) - 010101010010 etc
