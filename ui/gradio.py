import gradio as gr
from core.downloader import VideoDownloader
import json


def prase_video_info(info: dict):
    titles = []
    if info.get("entries"):
        for entry in info.get("entries"):
            titles.append(entry.get("title"))
            print(entry.get("title"))
    else:
        titles.append(info.get("title"))
    return titles


class VideoDownloaderApp:
    def __init__(self, downloader: VideoDownloader):
        self.downloader = VideoDownloader()

    def get_video_info(self, url: str):
        info = self.downloader.parse_video(url)
        titles = prase_video_info(info)
        return titles

    def create(self):
        with gr.Blocks(title="视频下载工具") as instance:
            with gr.Row():
                gr.Markdown("""
                        # 🎥 视频下载工具

                        支持查看视频信息，下载字幕和音频。
                        """)
            with gr.Column():
                url_input = gr.Textbox(
                    label="视频URL",
                    placeholder="请输入视频链接",
                )
                get_info_btn = gr.Button("📋 获取信息", variant="primary")
                info_output = gr.Textbox(label="视频信息", lines=10)
            # 绑定
            get_info_btn.click(
                fn=self.get_video_info,
                inputs=[url_input],
                outputs=[info_output]
            )
        return instance

    def launch(self, server_port: int = 7860):
        """启动界面"""
        instance = self.create()
        instance.launch(server_port=server_port)
