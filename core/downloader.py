import yt_dlp

# 视频下载器


class VideoDownloader:
    def __init__(self, quiet: bool = False):
        self.quiet = quiet
        self.video_url = None

    # 视频解析
    def parse_video(self, url: str):
        self.video_url = url
        with yt_dlp.YoutubeDL({'quiet': True}) as ydl:
            info = ydl.extract_info(self.video_url, download=False)
            return info

    # 字幕下载
    def download_subtitle(self, url: str):
        with yt_dlp.YoutubeDL({'quiet': True}) as ydl:
            ydl.download([url])

    # 音频下载
    def download_audio(self, selected_row: dict, url: str):
        print(selected_row)
        with yt_dlp.YoutubeDL({'quiet': True}) as ydl:
            ydl.download([url])
