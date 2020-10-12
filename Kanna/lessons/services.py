import os
import argparse


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
    from pydub import AudioSegment

    file_dir = r'C:\Users\zhuwe\OneDrive\Desktop\idea ink voice recordings'
    formats_to_convert = ['.m4a']
    two_minutes = 120000
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