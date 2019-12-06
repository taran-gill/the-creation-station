import io
import os

from google.cloud import speech
from google.cloud.speech import enums
from google.cloud.speech import types

def analyze_text(filepath):
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "./../../../Creation-Station-fb047bcb7c0b.json"

    # Instantiates a client
    client = speech.SpeechClient()

    # The name of the audio file to transcribe
    file_name = os.path.join(
        os.path.dirname(__file__),
        filepath)

    # Loads the audio into memory
    with io.open(file_name, 'rb') as audio_file:
        content = audio_file.read()
        audio = types.RecognitionAudio(content=content)

    config = types.RecognitionConfig(
        encoding=enums.RecognitionConfig.AudioEncoding.ENCODING_UNSPECIFIED,
        sample_rate_hertz=16000,
        language_code='en-US')

    # Detects speech in the audio file
    response = client.recognize(config, audio)

    for result in response.results:
        print('Transcript: {}'.format(result.alternatives[0].transcript))


if __name__ == '__main__':
    file = 'five_words.mp3' 

    script_path = os.path.abspath(os.path.join(__file__, '../../../', 'fixtures/'))
    file_path = os.path.join(script_path, file)

    analyze_text(file_path)
