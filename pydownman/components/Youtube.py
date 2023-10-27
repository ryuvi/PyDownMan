from pytube import YouTube, Playlist

class YTDownload:
    def __init__(self, url):
        self._url = url
    
    def download(self):
        yt = YouTube(self._url)
        yt.first().download()
