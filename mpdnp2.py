"""
  :Author: Henning Hasemann <hhasemann [at] web [dot] de>

  30-01-2009 -- Adapted for Weechat 0.3.0 By Bonzodog
  (bonzodog01 [at] gmail [dot] com)

  :What it does:
    This plugin lets you inform all users in the current
    channel about the song which music-player-daemon (MPD)
    is currently playing.

  :Usage:
    /mpdnp - Display file mpd is playing to current channel.

  :Configuration Variables:
    ============= ==========================================
    Variable name Meaning
    ============= ==========================================
    host          The host where your mpd runs
    port          The port to connect to mpd (usually 6600)
    format        How this script should display
                  whats going on.
                  You may use the following variables here:
                  $artist, $title_or_file,
                  $length_min, $length_sec, $pct,
                  $pos_min, $pos_sec
  
  Released under GPL licence.
"""

todo = """
  - maybe support sending commands to mpd.
  - maybe make condional display
    (displaying some characters only
     if preceding or trailing variables are set)
"""

import weechat as wc
import mpd
import re
from os.path import basename, splitext

import getsong

default_fmt = "/me 's MPD plays: {artist} - {title_or_file} ({url})"

wc.register("mpdnp2", "Quasar Jarosz", "0.6", "GPL", "np for mpd, 2", "", "")

def np(data, buffer, args):
  """
    Send information about the currently
    played song to the channel.
  """
  host = wc.config_get_plugin("host")
  port = int(wc.config_get_plugin("port"))
  client = mpd.MPDClient()
  client.connect(host, port)
  song = client.currentsong()
  
  # insert artist, title, album, track, path
  
  song_search_name = "{} - {}".format(song['artist'], song['title'])
  url = getsong.get_song_url(song_search_name)

  song.update({
      "title_or_file": song['title'] or splitext(basename(song['file']))[0],
      "url": url,
  })

  song_text = wc.config_get_plugin("format").format(**song)
  wc.command(wc.current_buffer(), song_text)
  
def dbgnp(data, buffer, args):
  try:
    return np(data, buffer, args)
  except Exception, e:
    print e
  
wc.hook_command("mpdnp", "now playing", "", np.__doc__, "", "np", "")

findvar = re.compile(r'[^\\]\$([a-z_]+)(\b|[^a-z_])')

default = {
  "host": "localhost",
  "port": "6600",
  "format": default_fmt,
}

for k, v in default.items():
  if not wc.config_get_plugin(k):
    wc.config_set_plugin(k, v)


