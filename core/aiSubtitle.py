import whisper
import json


def write_to_file(text: str, file_path: str):
    with open(file_path, "w") as f:
        f.write(text)


class SubtitleConverter:
    def __init__(self):
        self.model = whisper.load_model("turbo")

    def convert_subtitle(self, audio_path: str):
        result = self.model.transcribe(audio_path)
        write_to_file(json.dumps(result), "result.json")
        text_list = [i["text"] for i in result["segments"]]
        # text_list 去重
        text_list_uniq = sorted(list(set(text_list)), key=text_list.index)
        return "\n".join(text_list_uniq)
