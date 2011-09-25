from pyechonest import config, song, track, catalog, playlist
import settings

config.ECHO_NEST_API_KEY=settings.api_key

def get_track_data(t):
	print "getting track data for %s" % t
	data = [t.beats, t.bars, t.tatums, t.segments]
	list_of_lists = []
	list_type = type([])
	for data_type in data:
		list_of_floats = []
		for row in data_type:
			for key, value in row.iteritems():
				if type(value) == list_type:
					for item in value:
						list_of_floats.append(item)
				else:
					# It should be a float
					list_of_floats.append(value)
		list_of_lists.append(list_of_floats)
	return list_of_lists

# Given a catalog ID, it will return 4 songs from that catalog
def get_catalog_tracks(variety=0.8):
	print "getting catalog tracks"
	p = playlist.static(type='catalog-radio', seed_catalog=settings.seed_catalog, variety=variety, results=100) # lol
	print "done getting catalog tracks"
	tracks = []
	while len(tracks) < settings.songs_per_keystream:
		try:
			#s = p.get_next_song()
			s = p.pop()
			t = track.track_from_id(s.get_tracks('7digital')[0]['id'])
			tracks.append(t)
			print t
		except IndexError:
			pass
		if len(p) == 0:
			p = playlist.static(type='catalog-radio', seed_catalog=settings.seed_catalog, variety=variety, results=100)

	return tracks
