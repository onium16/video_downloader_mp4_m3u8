import os 
import requests
from urllib.parse import urlparse
import subprocess

'''
The script is based on the ffmpeg program.
For the script to work, download and place in the working folder 
ffmpeg-6.0-essentials_build, or another version of the program, 
but in this case it is necessary to make changes to the program 
settings by specifying the correct path to the program executable file.
'''

print("Enter the link video for download:")
link = input()


if "mp4" in link:
    '''
    Downloading videos from links containing 'mp4'
    '''
    print("mp4")
    
    # Get the filename from the URL
    url_parsed = urlparse(link)
    filename = os.path.basename(url_parsed.path)

    save_directory = os.path.dirname(os.path.abspath(__file__)) + '\\videos\\mp4'
    os.makedirs(save_directory, exist_ok=True)
    save_path = os.path.join(save_directory, filename + ".mp4")
    print(save_path)
    counter = 1
    while os.path.exists(save_path):
        # Increment the counter and modify the filename
        counter += 1
        filename_with_counter = f"{os.path.splitext(filename)[0]}_{counter}.mp4"
        save_path = os.path.join(save_directory, filename_with_counter)

    def download_video(url, save_path):
        response = requests.get(url, stream=True)
        response.raise_for_status()

        with open(save_path, 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    file.write(chunk)

        print(f"Video downloaded successfully! File saved in path: {save_path}")


    download_video(link, save_path)


if "m3u8" in link:
    '''
    Download videos from links containing 'm3u8'
    '''
    print("m3u8")

    # Path to ffmpeg executable
    ffmpeg_path = os.path.dirname(os.path.abspath(__file__))
    print(ffmpeg_path)
    executable_ffmpeg_file = os.path.join(ffmpeg_path, 'ffmpeg-6.0-essentials_build', 'bin', 'ffmpeg.exe')
    print(executable_ffmpeg_file)

    # Get the filename from the URL
    url_parsed = urlparse(link)
    filename = os.path.basename(url_parsed.path)

    save_directory = os.path.dirname(os.path.abspath(__file__)) + '\\videos\\m3u8'
    os.makedirs(save_directory, exist_ok=True)
    save_path = os.path.join(save_directory, os.path.splitext(filename)[0] + ".mp4")
    print(save_path)
    counter = 1
    while os.path.exists(save_path):
        # Increment the counter and modify the filename
        counter += 1
        filename_with_counter = f"{os.path.splitext(filename)[0]}_{counter}.mp4"
        save_path = os.path.join(save_directory, filename_with_counter)


    # Downloading and merging streams
    command = [
        executable_ffmpeg_file,
        '-i', 
        link,
        '-c', 
        'copy',
        '-protocol_whitelist', 
        'file,http,https,tcp,tls',
        save_path
    ]

    subprocess.run(command)

    print(f"Video downloaded successfully! File saved in path: {save_path}")
