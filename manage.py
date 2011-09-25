import sys
from lib import personal_catalog_scanner
from lib import keystreams

#N6E4NIOVYMTHNDM8J
def error(message):
	print message
	print "Usage: python manage.py [setup|new|add|delete|info]"
	exit(1)

if len(sys.argv) < 2:
	error("You must enter a mode.")

mode = sys.argv[1]
if mode == "setup":
	print "If you wish to use your own echonest API key and thus use your own personalised music catalog as a seed, please cancel the setup, copy your API key into settings.py, then re-run the setup. Otherwise, you will have to use a default seed catalog."
	cancel = raw_input("Cancel? y/n: ").strip()
	if cancel == "y":
		error("Replace the existing api_key with your own in settings.py, then re-run python manage.py setup.")
	else:
		music_dir = raw_input("Enter the absolute path to your music directory.").strip()
		personal_catalog_scanner.run("library", music_dir)
		print "Replace the existing seed_catalog_id in settings.py with the one generated above. After that, run python manage.py add to add a keystream."
elif mode == "new":
	print "Generating a new random key"
	print "---------------------------"
	keystream_name = raw_input("Name of keystream: ").strip()
	new_keystream = keystreams.Keystream(keystream_name)
	print "Successfully added new keystream. Total number of keystreams: %d" % len(keystreams.total)
	print "To encypt a message using this keystream, run python echocrypt.py e \"message to encrypt\" \"%s\"" % keystream_name
elif mode == "add":
	print "Create a key based on a specific list of tracks"
	print "Enter the ID of each track, followed by a new line. Enter an empty line to stop."
	track_ids = []
	# So terrible
	track_id = raw_input("Track ID: ").strip()
	track_ids.append(track_id)

	while track_id != '':
		track_id = raw_input("Track ID: ").strip()
		track_ids.append(track_id)
	# Now create a new keystream from those track IDs
	keystream_name = raw_input("Name of keystream: ").strip()
	new_keystream = keystreams.Keystream(keystream_name, track_ids=track_ids)
	print "Successfully added new keystream. Total number of keystreams: %d" % len(keystreams.total)
elif mode == "delete":
	keystream_name = raw_input("Name of keystream to delete: ")
	keystream = keystreams.total[keystream_name].delete()
elif mode == "info":
	# Shows you the keystreams you have, and how many characters you have left on each of them
	print "Total number of keystreams: %d" % len(keystreams.total)
	for keystream in keystreams.total:
		print keystream
		print "---------"
		print "Tracks:" 
		for track in keystreams.total[keystream].tracks:
			print "Artist: %s; Song: %s; ID: %s" % (track.artist, track.title, track.id)
		print "Number of characters left: %d" % keystreams.total[keystream].get_chars_left()
		print
else:
	error("Invalid mode.")
