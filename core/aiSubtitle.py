import whisper


class SubtitleConverter:
    def __init__(self):
        self.model = whisper.load_model("turbo")

    def convert_subtitle(self, audio_path: str):
        result = self.model.transcribe(audio_path)
        text_list = [i["text"] for i in result["segments"]]
        # text_list 去重
        text_list = list(set(text_list))
        return "\n".join(text_list)
