import sys

if __name__ == '__main__':
	sys.path.insert(0,'..')

import logging
import argparse
import re
from youtube import Video, PlayList, __version__, __github__

class main:
	'''
	This is main cli class for youtube.py
	'''
	def __init__(self):
		self.args = self.process_args()

		self.url = self.check_url(self.args.url)

		self.conn = self.args.connections

		if "playlist" in self.url:
			self.PlayList = True
			self.videos = [f"https://youtu.be/{n['vid']}" for n in PlayList(self.url).get_dict]
		else:
			self.PlayList = False
			self.videos = list([self.url])

		if self.args.output:
			self.output = self.args.output
		else:
			self.output = ""

		if self.args.logs:
			self.process_logg()

		if self.args.streams:
			self.print_streams()

		if self.args.ffmpeg:
			self.process_ffmpeg()

		if self.args.video:
			self.process_video()
		
		if self.args.itag:
			self.process_itag()

		if self.args.audio:
			self.process_audio()

		if self.args.resolution:
			self.process_resolution()
		exit()

	def print_streams(self):
		if self.args.streams:
			for n in self.videos:
				print(f'Video url: {n}')
				for m in Video(n).streams:
					print(m)