from ui import VideoDownloaderApp
from core.downloader import VideoDownloader
if __name__ == "__main__":
    v = VideoDownloader()
    app = VideoDownloaderApp(downloader=v)
    demo = app.create()
    # 9980端口
    demo.launch(server_port=9980)
