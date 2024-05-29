import io
import subprocess

from google.oauth2 import service_account
from google.cloud import speech

client_file = 'transcriber.json'
credentials = service_account.Credentials.from_service_account_file(client_file)
client = speech.SpeechClient(credentials=credentials)


# gcs_uri = 'gcs:<uri link>
# config = speech.RecognitionConfig(
#     encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
#     sample_rate_hertz=44100,
#     language_code='en-US',  # Corrected field name
#     model='video'
# )
# audio = speech.RecognitionAudio(uri=gcs_uri)
# operation = client.long_running_recognize(config=config, audio=audio)
# print("Waiting for operation to complete")
#response = operation.results(timeout=200)
# for result in response.results:
#   print(result.alternatives[0].transcript)





audio_file = 'Video to transcribe.wav'
mono_audio_file = 'Mono Audio.wav'

# Convert the stereo audio file to mono using ffmpeg
subprocess.run(['ffmpeg', '-i', audio_file, '-ac', '1', mono_audio_file])

with io.open(mono_audio_file, 'rb') as f:
    content = f.read()
    audio = speech.RecognitionAudio(content=content)

config = speech.RecognitionConfig(
    encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
    sample_rate_hertz=44100,
    language_code='en-US',  # Corrected field name
    model='video'
)

response = client.recognize(config=config, audio=audio)
for result in response.results:
    print(result.alternatives[0].transcript)

