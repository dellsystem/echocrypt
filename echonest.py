from pyechonest import config
config.ECHO_NEST_API_KEY="EAEJJFF8SZIGOKH2J"
from pyechonest import song, track

def get_track(artist, title):
	s = song.search(artist=artist, title=title, buckets=['id:7digital', 'tracks'], limit=True)[0]
	t_id = s.get_tracks('7digital')[0]['id']
	t = track.track_from_id(t_id)
	return t
