from azure.identity import DefaultAzureCredential
import azure.cognitiveservices.speech as speech_sdk

# Foundry Cognitive Services endpoint
endpoint = "https://<your-foundry-resource>.cognitiveservices.azure.com/"

# Authenticate using Entra ID
credential = DefaultAzureCredential()

speech_config = speech_sdk.SpeechConfig(
    token_credential=credential,
    endpoint=endpoint
)

# Save synthesized speech to a file
audio_config = speech_sdk.audio.AudioOutputConfig(filename="ssml_output.wav")

# Create Speech Synthesizer
speech_synthesizer = speech_sdk.SpeechSynthesizer(
    speech_config=speech_config,
    audio_config=audio_config
)

# SSML content
ssml = """
<speak version="1.0"
       xmlns="http://www.w3.org/2001/10/synthesis"
       xmlns:mstts="https://www.w3.org/2001/mstts"
       xml:lang="en-US">

    <voice name="en-US-AriaNeural">
        <mstts:express-as style="cheerful">
            Welcome to Azure AI Speech!
        </mstts:express-as>
    </voice>

    <voice name="en-US-GuyNeural">
        I say
        <phoneme alphabet="sapi" ph="t ao m ae t ow">
            tomato
        </phoneme>.
        <break strength="medium"/>
        Let's learn Speech Synthesis Markup Language.
    </voice>

</speak>
"""

# Synthesize SSML
result = speech_synthesizer.speak_ssml_async(ssml).get()

# Display result
if result.reason == speech_sdk.ResultReason.SynthesizingAudioCompleted:
    print("SSML speech synthesized successfully!")
    print("Audio saved as: ssml_output.wav")
elif result.reason == speech_sdk.ResultReason.Canceled:
    cancellation = result.cancellation_details
    print("Speech synthesis canceled.")
    print("Reason:", cancellation.reason)
    if cancellation.error_details:
        print("Error details:", cancellation.error_details)