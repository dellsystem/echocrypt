import sys
from lib import personal_catalog_scanner
from lib import keystreams

#N6E4NIOVYMTHNDM8J
def error(message):
	print message
	print "Usage: python manage.py [setup|add|delete|info]"
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
elif mode == "add":
	keystream_name = raw_input("Name of keystream: ").strip()
	new_keystream = keystreams.Keystream(keystream_name)
	print "Successfully added new keystream. Total number of keystreams: %d" % len(keystreams.total)
	print "To encypt a message using this keystream, run python echocrypt.py e \"message to encrypt\" \"%s\"" % keystream_name
elif mode == "delete":
	keystream_name = raw_input("Name of keystream to delete: ")
	keystream = keystreams.total[keystream_name].delete()
elif mode == "info":
	# Shows you the keystreams you have, and how many characters you have left on each of them
	print "Total number of keystreams: %d" % len(keystreams.total)
	for keystream in keystreams.total:
		print keystream
		print "---------"
		print "Number of characters left: %d" % keystreams.total[keystream].get_chars_left()
else:
	error("Invalid mode.")
