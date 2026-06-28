from azure.identity import DefaultAzureCredential
import azure.cognitiveservices.speech as speech_sdk

# Foundry Cognitive Services endpoint
endpoint = "https://<your-foundry-resource>.cognitiveservices.azure.com/"

# Authenticate
credential = DefaultAzureCredential()

# Translation configuration
translation_config = speech_sdk.translation.SpeechTranslationConfig(
    token_credential=credential,
    endpoint=endpoint
)

# Source language
translation_config.speech_recognition_language = "en-US"

# Target languages
translation_config.add_target_language("fr")
translation_config.add_target_language("ja")

# Use default microphone
audio_config = speech_sdk.AudioConfig(use_default_microphone=True)

# Translation Recognizer
translator = speech_sdk.translation.TranslationRecognizer(
    translation_config=translation_config,
    audio_config=audio_config
)

print("Speak now...")

# Translate
result = translator.recognize_once_async().get()

if result.reason == speech_sdk.ResultReason.TranslatedSpeech:

    print("Original Text :", result.text)

    print("\nTranslations:")
    for language, translation in result.translations.items():
        print(f"{language} : {translation}")

else:
    print("Translation Failed:", result.reason)