if __name__ == '__main__':
    import io
    import os

    # Imports the Google Cloud client library
    from google.cloud import speech

    credential_path = r"C:\Users\zhuwe\OneDrive\Desktop\Speech Recognition\My First Project-47f430b8a379.json"
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credential_path

    # Instantiates a client
    client = speech.SpeechClient()

    # The name of the audio file to transcribe
    file_name = os.path.join(r"C:\Users\zhuwe\OneDrive\Desktop\idea ink voice recordings\unprocessed",
                             "Seet DC Circuits 01(1).wav")


    def transcribe_file(speech_file):
        """Transcribe the given audio file asynchronously."""
        from google.cloud import speech

        client = speech.SpeechClient()

        with io.open(speech_file, "rb") as audio_file:
            content = audio_file.read()

        audio = speech.RecognitionAudio(content=content)
        config = speech.RecognitionConfig(
            encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
            sample_rate_hertz=16000,
            language_code="en-US",
        )

        operation = client.long_running_recognize(
            request={"config": config, "audio": audio}
        )

        print("Waiting for operation to complete...")
        response = operation.result(timeout=90)

        # Each result is for a consecutive portion of the audio. Iterate through
        # them to get the transcripts for the entire audio file.
        for result in response.results:
            # The first alternative is the most likely one for this portion.
            print(u"Transcript: {}".format(result.alternatives[0].transcript))
            print("Confidence: {}".format(result.alternatives[0].confidence))

    transcribe_file(file_name)