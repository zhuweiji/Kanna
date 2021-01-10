import os
import io
import argparse

from pydub import AudioSegment
import wave

from google.cloud import speech
from google.cloud import storage

bucketname = "kanna_speech_bucket"

#   for a credentials json file in the same dir as this .py file
credential_path = os.path.join(os.getcwd(), 'booming-skill-282713-ebdebd62f7e3.json')

#   running manage.py means that cwd is one level above credentials file
if not os.path.isfile(credential_path): credential_path = os.path.join(os.getcwd(), 'lessons',
                                                                       'booming-skill-282713-ebdebd62f7e3.json')
if not os.path.isfile(credential_path): credential_path = r'/home/zhuweiji/Kanna/Kanna/lessons/' \
                                                          r'booming-skill-282713-ebdebd62f7e3.json'

#   saves json credentials to local env variable
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credential_path


def mp3_to_wav(audio_file_name):
    if audio_file_name.split('.')[1] == 'mp3':
        sound = AudioSegment.from_mp3(audio_file_name)
        audio_file_name = audio_file_name.split('.')[0] + '.wav'
        sound.export(audio_file_name, format="wav")
    # elif audio_file_name.split('.')[1] == 'm4a':
    #     sound = AudioSegment.from_file(audio_file_name, )


def stereo_to_mono(audio_file_name):
    sound = AudioSegment.from_wav(audio_file_name)
    sound = sound.set_channels(1)
    sound.export(audio_file_name, format="wav")


def frame_rate_channel(audio_file_name):
    with wave.open(audio_file_name, "rb") as wave_file:
        frame_rate = wave_file.getframerate()
        channels = wave_file.getnchannels()
        return frame_rate,channels


def upload_blob(bucket_name, source_file_name, destination_blob_name):
    """Uploads a file to the bucket."""
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    blob.upload_from_filename(source_file_name)


def delete_blob(bucket_name, blob_name):
    """Deletes a blob from the bucket."""
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob(blob_name)

    blob.delete()


def google_transcribe(filepath):
    print("running google cloud transcription...")

    if not os.path.isfile(filepath): raise FileNotFoundError("filepath is invalid")
    if not os.path.isfile(credential_path): raise FileNotFoundError(f"credentials path {credential_path} is not valid")

    print('checking/converting audio file')
    mp3_to_wav(filepath)

    # The name of the audio file to transcribe

    frame_rate, channels = frame_rate_channel(filepath)

    if channels > 1:
        stereo_to_mono(filepath)

    bucket_name = bucketname
    source_file_name = filepath
    destination_blob_name = os.path.basename(filepath)

    print('uploading audio to cloud')
    upload_blob(bucket_name, source_file_name, destination_blob_name)

    gcs_uri = 'gs://' + bucketname + '/' + destination_blob_name
    transcript = ''

    client = speech.SpeechClient()
    audio = speech.RecognitionAudio(uri=gcs_uri)

    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=frame_rate,
        language_code='en-SG')

    # Detects speech in the audio file
    print("beginning transcription")
    operation = client.long_running_recognize(config=config, audio=audio)
    response = operation.result()

    for result in response.results:
        transcript += result.alternatives[0].transcript

    delete_blob(bucket_name, destination_blob_name)
    print('audio deleted from cloud')
    print('transcription completed')
    return transcript


def listify(arr):
    """ convert from db str representation to list
        for all values inside, convert all from str to int"""
    if not isinstance(arr, list):
        arr = arr.strip('][').split(', ')

    # arr = [i.strip(" ' ") if isinstance(i, str) else i for i in arr]
    for i in arr:
        if isinstance(i, str):
            try:
                arr[arr.index(i)] = int(i.strip("'"))
            except ValueError:
                pass
    return arr


if __name__ == '__main__':
    print(google_transcribe(r'C:\Users\zhuwe\OneDrive\Desktop\audio_files\unprocessed\matthew.wav'))

    if False:
        from pydub import AudioSegment

        # file_dir = r'C:\Users\zhuwe\OneDrive\Desktop\idea ink voice recordings'
        file_dir = r'C:\Users\zhuwe\OneDrive\Desktop\audio_files'
        formats_to_convert = ['.m4a']
        two_minutes = 120000/2
        unprocessed_dir = os.path.join(file_dir, 'unprocessed')
        processed_dir = os.path.join(file_dir, 'processed')

        for (dirpath, dirnames, filenames) in os.walk(unprocessed_dir):
            for filename in filenames:
                if filename.endswith(tuple(formats_to_convert)):
                    filepath = dirpath + '/' + filename
                    (path, file_extension) = os.path.splitext(filepath)
                    file_extension_final = file_extension.replace('.', '')
                    try:
                        track = AudioSegment.from_file(filepath,
                                                       file_extension_final)
                        wav_filename = filename.replace(file_extension_final, 'wav')
                        wav_path = dirpath + '/' + wav_filename
                        print('CONVERTING: ' + str(filepath))
                        file_handle = track.export(wav_path, format='wav')
                        os.remove(filepath)
                    except Exception as E:
                        print("ERROR CONVERTING " + str(filepath))
                        raise E

        for (dirpath, dirnames, filenames) in os.walk(unprocessed_dir):
            for filename in filenames:
                path = os.path.join(dirpath, filename)
                track = AudioSegment.from_file(path, 'm4a')
                (filepath, file_extension) = os.path.splitext(path)
                (filename, file_extension) = os.path.splitext(filename)
                num = 1
                while track.duration_seconds > 120:
                    part, second_part = track[:two_minutes], track[two_minutes:]
                    part_name = os.path.join(processed_dir, filename) + f'part{num}' + file_extension
                    part.export(part_name, format='wav')
                    track = second_part
                    num += 1
                track_name = os.path.join(processed_dir, filename) + f'part{num}' + file_extension
                print(track_name)
                track.export(track_name, format='wav')
        print('Success!')