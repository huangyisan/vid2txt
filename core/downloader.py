import yt_dlp
import os


class VideoDownloader:
    def __init__(self, quiet: bool = False):
        self.quiet = quiet
        self.video_url = None

    # 视频解析
    def parse_video(self, url: str):
        self.video_url = url
        with yt_dlp.YoutubeDL({'quiet': True, 'cookiefile': f'{os.getcwd()}/cookies.txt', }) as ydl:
            info = ydl.extract_info(self.video_url, download=False)
            return info

    # 字幕下载
    def download_subtitle(self, url: str):
        with yt_dlp.YoutubeDL({'quiet': True}) as ydl:
            ydl.download([url])

    # 音频下载
    def download_audio(self, selected_row: int, outtmpl: str):
        ydl_opts = {'format': 'bestaudio/best',
                    'cookiefile': f'{os.getcwd()}/cookies.txt',
                    'playlist_items': f'{selected_row+1}',
                    'postprocessors': [{'key': 'FFmpegExtractAudio',
                                        'nopostoverwrites': False,
                                        'preferredcodec': 'best',
                                        'preferredquality': '5'}], 'outtmpl': {'default': f'{outtmpl}'}}
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([self.video_url])
