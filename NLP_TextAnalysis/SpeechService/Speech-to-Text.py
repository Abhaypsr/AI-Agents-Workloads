from azure.identity import DefaultAzureCredential
import azure.cognitiveservices.speech as speech_sdk

# Foundry Cognitive Services endpoint
endpoint = "https://<your-foundry-resource>.cognitiveservices.azure.com/"

# Authenticate
credential = DefaultAzureCredential()

speech_config = speech_sdk.SpeechConfig(
    token_credential=credential,
    endpoint=endpoint
)

# Audio file
audio_config = speech_sdk.audio.AudioConfig(filename="audio.wav")

# Speech Recognizer
speech_recognizer = speech_sdk.SpeechRecognizer(
    speech_config=speech_config,
    audio_config=audio_config
)

# Transcribe
result = speech_recognizer.recognize_once_async().get()

if result.reason == speech_sdk.ResultReason.RecognizedSpeech:
    print("Transcription:", result.text)
else:
    print("Recognition Failed:", result.reason)