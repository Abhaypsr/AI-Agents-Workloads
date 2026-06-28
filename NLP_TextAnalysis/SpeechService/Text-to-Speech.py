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

# Choose Voice
speech_config.speech_synthesis_voice_name = "en-US-Serena:DragonHDLatestNeural"

# Output file
audio_config = speech_sdk.audio.AudioOutputConfig(filename="output.wav")

# Speech Synthesizer
speech_synthesizer = speech_sdk.SpeechSynthesizer(
    speech_config=speech_config,
    audio_config=audio_config
)

text = "Hello! Welcome to Azure AI Speech."

# Synthesize
result = speech_synthesizer.speak_text_async(text).get()

if result.reason == speech_sdk.ResultReason.SynthesizingAudioCompleted:
    print("Speech generated successfully!")
    print("Saved as output.wav")
else:
    print("Speech synthesis failed:", result.reason)