import whisper


class SubtitleConverter:
    def __init__(self):
        self.model = whisper.load_model("turbo")

    def convert_subtitle(self, audio_path: str):
        result = self.model.transcribe(audio_path)
        return result["text"]
