from pyechonest import config
config.ECHO_NEST_API_KEY="EAEJJFF8SZIGOKH2J"
from pyechonest import song, track, catalog, playlist
# CAFAHCC1329DCB5C35 catalogue thing lol

def get_track_data(t):
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
def get_catalog_tracks(catalog_id, n=4, variety=0.8):
	p = playlist.Playlist(type='catalog-radio', seed_catalog=catalog_id, variety=variety)
	tracks = []
	while len(tracks) < n:
		try:
			s = p.get_next_song()
			t = track.track_from_id(s.get_tracks('7digital')[0]['id'])
			tracks.append(t)
		except IndexError:
			pass

	return tracks
