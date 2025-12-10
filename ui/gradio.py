import gradio as gr
from core.downloader import VideoDownloader
import json
import pandas as pd


def parse_video_info(info: dict):
    video_info = []
    if info.get("entries"):
        for entry in info.get("entries"):
            video_info.append(
                {
                    "title": entry.get("title"),
                    "uploader": entry.get("uploader"),
                }
            )

    else:
        video_info.append(
            {
                "title": info.get("title"),
                "uploader": info.get("uploader"),
            }
        )
    print(video_info)
    res = pd.DataFrame(video_info)
    res.columns = ["标题", "上传者"]
    print(res)
    return res


class VideoDownloaderApp:
    def __init__(self, downloader: VideoDownloader):
        self.downloader = VideoDownloader()

    def get_video_info(self, url: str):
        info = self.downloader.parse_video(url)
        titles = parse_video_info(info)
        return titles

    def download_audio(self, selected_row_state: dict):
        print(selected_row_state)
        if not selected_row_state:
            return gr.Error("请选择要下载的音频")
        return selected_row_state
        # subtitle_url = selected_row.get("title", "")
        # audio_url = selected_row.get("audio_url", "")
        # title = selected_row.get("title", "")
        # self.downloader.download_audio(selected_row)

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

                # 选中内容
                selected_row_state = gr.State(None)
                get_info_btn = gr.Button("📋 获取信息", variant="primary")
                info_output = gr.Dataframe(
                    label="视频信息",
                    headers=["标题", "上传者"],
                    datatype=["str", "str"],
                )
                download_btn = gr.Button("📥 下载选中项", variant="primary")
                download_output = gr.Textbox(label="下载结果", visible=True)
                selected = gr.Number(label="选中索引", visible=True)
                selected_row = gr.Textbox(label="选中内容", visible=True)
                download_to_index = gr.Number(label="下载到索引", visible=True)

            def get_selected_index(evt: gr.SelectData):
                return evt.index[0]

            # 绑定
            get_info_btn.click(
                fn=self.get_video_info,
                inputs=[url_input],
                outputs=info_output
            )

            # 更新 state
            info_output.select(
                fn=get_selected_index,
                inputs=None,
                outputs=[selected_row_state]
            )
            # 显示索引用于调试
            info_output.select(
                fn=get_selected_index,
                inputs=None,
                outputs=[selected]
            )

            # 下载按钮
            download_btn.click(
                fn=self.download_audio,
                inputs=[selected_row_state],
                outputs=download_output
            )

        return instance

    def launch(self, server_port: int = 7860):
        """启动界面"""
        instance = self.create()
        instance.launch(server_port=server_port)
