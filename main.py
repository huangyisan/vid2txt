from ui import VideoDownloaderApp
from core.downloader import VideoDownloader
if __name__ == "__main__":
    v = VideoDownloader()
    app = VideoDownloaderApp(downloader=v)
    demo = app.create()
    demo.launch()
