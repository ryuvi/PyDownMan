from collections import OrderedDict
from bencoding import Encoder, Decoder
from requests import req
from os import path
import random


class TorrentDownload:
    def __init__(self, url):
        if path.isfile(url):
            with open(url, 'rb') as f:
                meta_info = f.read()
                torrent = Decoder(meta_info).decode()
        else:
            pass
