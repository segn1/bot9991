
import yt_dlp
from config import DOWNLOAD_PATH

def download_video(url):
    ydl_opts = {
        'outtmpl': f'{DOWNLOAD_PATH}%(title)s.%(ext)s',
        'format': 'best'
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        file = ydl.prepare_filename(info)

    return file
