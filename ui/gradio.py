import gradio as gr
from core.downloader import VideoDownloader
from core.aiSubtitle import SubtitleConverter
import pandas as pd
import os


class VideoDownloaderApp:
    def __init__(self, downloader: VideoDownloader):
        self.downloader = VideoDownloader()
        self.aiSubtitle = SubtitleConverter()
        self.video_info = None

    def parse_video_info(self, info: dict):
        video_info = []
        if info.get("entries"):
            for entry in info.get("entries"):
                video_info.append(
                    {
                        "title": entry.get("title"),
                        "uploader": entry.get("uploader"),
                        "video_id": entry.get("id"),
                    }
                )

        else:
            video_info.append(
                {
                    "title": info.get("title"),
                    "uploader": info.get("uploader"),
                    "video_id": info.get("id"),
                }
            )
        print(video_info)
        res = pd.DataFrame(video_info)
        res.columns = ["标题", "上传者", "视频ID"]
        self.video_info = res

    def get_video_info(self, url: str):
        info = self.downloader.parse_video(url)
        self.parse_video_info(info)
        return self.video_info

    def download_audio(self, selected_row_state: int):
        outtmpl = f"{self.video_info.iloc[selected_row_state]['视频ID']}.m4a"
        if selected_row_state is None or selected_row_state == "":
            return gr.Error("请选择要下载的音频")
        self.downloader.download_audio(selected_row_state, outtmpl)
        return os.path.join(
            os.getcwd(), outtmpl)

        # subtitle_url = selected_row.get("title", "")
        # audio_url = selected_row.get("audio_url", "")
        # title = selected_row.get("title", "")
        # self.downloader.download_audio(selected_row)

    def get_ai_subtitle(self, download_output: str):
        subtitle = self.aiSubtitle.convert_subtitle(download_output)
        return subtitle

    def create(self):
        with gr.Blocks(title="视频下载工具") as instance:
            with gr.Row():
                gr.Markdown("""
                        # 🎥 视频下载工具

                        支持查看视频信息，下载字幕和音频。
                        """)
            # 内容排版
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
                    headers=["标题", "上传者", "视频ID"],
                    datatype=["str", "str", "str"],
                )
                download_btn = gr.Button("📥 下载选中项", variant="primary")
                download_output = gr.File(label="下载结果", visible=True)
                get_ai_subtitle_btn = gr.Button("📥 获取AI字幕", variant="primary")
                ai_subtitle_output = gr.Textbox(label="AI字幕", visible=True)
                selected = gr.Number(label="选中索引", visible=True)

            # 事件定义
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

            get_ai_subtitle_btn.click(
                fn=self.get_ai_subtitle,
                inputs=[download_output],
                outputs=ai_subtitle_output
            )
        return instance

    def launch(self, server_port: int = 7860):
        """启动界面"""
        instance = self.create()
        instance.launch(server_port=server_port)
