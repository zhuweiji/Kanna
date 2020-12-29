import io
import os

#   for a credentials json file in the same dir as this .py file
credential_path = os.path.join(os.getcwd(), 'booming-skill-282713-ebdebd62f7e3.json')
#   running manage.py means that cwd is one level above credentials file
if not os.path.isfile(credential_path): credential_path = os.path.join(os.getcwd(), 'lessons', 'booming-skill-282713-ebdebd62f7e3.json')
if not os.path.isfile(credential_path): credential_path = r'/home/zhuweiji/Kanna/Kanna/lessons/booming-skill-282713-ebdebd62f7e3.json'
#   saves json credentials to local env variable
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credential_path


# def transcribe_file(speech_file):
#     """ transcribes a given audio filepath asynchrously via google cloud speech to text API """
#     try:
#         from google.cloud import speech
#     except Exception as E:
#         print("google.cloud speech module not installed. Try running pip install google-cloud-speech")
#         raise E
#
#     print('running google cloud to speech transcription')
#
#     client = speech.SpeechClient()
#
#     with io.open(speech_file, "rb") as audio_file:
#         content = audio_file.read()
#
#     audio = speech.RecognitionAudio(content=content)
#     config = speech.RecognitionConfig(
#         encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
#         sample_rate_hertz=16000,
#         language_code="en-US",
#     )
#
#     operation = client.long_running_recognize(
#         request={"config": config, "audio": audio}
#     )
#
#     print("Waiting for operation to complete...")
#     response = operation.result(timeout=90)
#
#     # Each result is for a consecutive portion of the audio. Iterate through
#     # them to get the transcripts for the entire audio file.
#     for result in response.results:
#         # The first alternative is the most likely one for this portion.
#         print(u"Transcript: {}".format(result.alternatives[0].transcript))
#         print("Confidence: {}".format(result.alternatives[0].confidence))


def transcribe_file(filepath):
    import speech_recognition as sr
    print("running google cloud transcription...")

    if not os.path.isfile(filepath): raise FileNotFoundError("filepath is invalid")
    if not os.path.isfile(credential_path): raise FileNotFoundError(f"credentials path {credential_path} is not valid")

    r = sr.Recognizer()

    with sr.AudioFile(filepath) as source:
        audio = r.record(source)

    import json

    with open(credential_path, "r") as rdr:
        _ = json.load(rdr)
        GOOGLE_CLOUD_SPEECH_CREDENTIALS = json.dumps(_)

    try:
        lang = ['en-SG', 'en-US', 'en-AU', 'en-CA', 'en-GH', 'en-HK', 'en-IN',
                'en-IE', 'en-KE', 'en-NZ', 'en-NG', 'en-PK', 'en-PH', 'en-ZA', 'en-TZ', 'en-GB']

        from difflib import SequenceMatcher

        def similar(a, b):
            return SequenceMatcher(None, a, b).ratio()

        # for i in range(val):
        #     print('language: ' + lang[i])
        #     print(res := r.recognize_google_cloud(audio, credentials_json=GOOGLE_CLOUD_SPEECH_CREDENTIALS, language=lang[i]))
        #     print('similarity: ', similar(master_str, res))

        output = r.recognize_google_cloud(audio, credentials_json=GOOGLE_CLOUD_SPEECH_CREDENTIALS, language='en-SG')
        print('transcription complete')
        return output

    except sr.UnknownValueError:
        print("Google Cloud Speech could not understand audio")
        return -1
    except sr.RequestError as e:
        raise e
        print("Could not request results from Google Cloud Speech service; {0}".format(e))
        return -2


if __name__ == '__main__':
    print(__file__ + " is running as main")
    print(credential_path)
    print(os.path.isfile(credential_path))
    foo = r'/home/zhuweiji/Kanna/Kanna/lessons/media/audio/Recording_4part1.wav'
    print(os.path.isfile(foo))
    val = transcribe_file(foo)
    print(val)
    # filename = r'Recording (4)part1.wav'
    # # filepath = os.path.join(r'C:\lessons\media\audio', filename)
    # filepath = os.path.join(r'C:\Users\zhuwe\OneDrive\Documents\Sound recordings\processed', filename)

    # master_str = "So pressure is the amount of force experienced per unit area so like we say here pressure is force in newtons divided per area in meter squared so you must take note that area must be in meter squared so the unit for pressure is pascal or mmhg so how do you calculate pressure so as we said before we take the force in newtons divided by area in meter squared so in this example its 3cm by 3cm area with a force of 10 newtons so again you convert the area to meter and then you get a net result of 0.0009Pascals or11100Pascal"
    # val = 2

    # transcribe_file(filepath)
