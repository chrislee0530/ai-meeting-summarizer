from __future__ import annotations
import time
import azure.cognitiveservices.speech as speechsdk

def transcribe_file(file_path: str, speech_key: str, region: str) -> str:
    if not speech_key or not region:
        raise RuntimeError("Missing SPEECH_KEY or SPEECH_REGION. Check your .env file.")
    
    speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=region)
    speech_config.speech_recognition_language = "en-CA"

    audio_config = speechsdk.audio.AudioConfig(filename=file_path)
    recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)

    all_text = []
    done = False

    def recognized_handler(event):
        if event.result.reason == speechsdk.ResultReason.RecognizedSpeech and event.result.text:
            all_text.append(event.result.text)

    def stop_handler(event):
        nonlocal done
        done = True

    recognizer.recognized.connect(recognized_handler)
    recognizer.session_stopped.connect(stop_handler)
    recognizer.canceled.connect(stop_handler)

    recognizer.start_continuous_recognition()
    while not done:
        time.sleep(0.5)
    recognizer.stop_continuous_recognition()

    return " ".join(all_text).strip()
