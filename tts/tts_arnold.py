from TTS.api import TTS

if __name__ == '__main__':
    # tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2", gpu=True)
    tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2")
    tts.tts_to_file(text="Hello, world!", file_path="output.wav", speaker_wav="/path/to/target/speaker.wav", language="en")
