import threading
import os
import yt_dlp
import sys

window = None
lbl_log = None
message = ''

active_downloads = set()
active_downloads_lock = threading.Lock()
progress_values = dict()

base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
ffmpeg_path = os.path.join(base_path, 'ffmpeg', 'bin', 'ffmpeg.exe')
ffmpeg_dir = os.path.dirname(ffmpeg_path)

def update_target_progress():
    if progress:
        with active_downloads_lock:
            if not progress_values:
                value = 0.0
            else:
                value = sum(progress_values.values()) / len(progress_values)
        window.after(0, lambda: progress.set(value))


def link_to_audio(url_audio):
    threading.Thread(target=download, args=(url_audio, True), daemon=True).start()


def link_to_video(url_video):
    threading.Thread(target=download, args=(url_video, False), daemon=True).start()


def download(url, is_audio):
    """
    installation via threading
    """
    key = (url, is_audio)
    with active_downloads_lock:
        if key in active_downloads:
            return
        active_downloads.add(key)
        progress_values[key] = 0.0

    download_path = os.path.join(os.path.expanduser("~"), "Downloads")
    output_folder = os.path.join(download_path, "Converted")
    os.makedirs(output_folder, exist_ok=True)

    def progress_hook(d):
        if d['status'] == 'downloading':
            total = d.get('total_bytes') or d.get('total_bytes_estimate')
            downloaded = d.get('downloaded_bytes', 0)
            with active_downloads_lock:
                progress_values[key] = (downloaded / total) if total else 0.0
        elif d['status'] == 'finished':
            with active_downloads_lock:
                progress_values[key] = 1.0
        update_target_progress()

    ydl_opts = {
        'format': 'bestaudio/best' if is_audio else 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/mp4',
        'outtmpl': os.path.join(output_folder, '%(title)s.%(ext)s'),
        'noplaylist': True,
        'quiet': True,
        'progress_hooks': [progress_hook],
        'ffmpeg_location': ffmpeg_dir,
    }

    if is_audio:
        ydl_opts['postprocessors'] = [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '320',
        }]

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        msg = f'Файл успешно скачан.\nПуть: {output_folder}'
    except Exception as e:
        msg = f'Ошибка при загрузке {url}:\n{str(e)}'
    finally:
        with active_downloads_lock:
            active_downloads.discard(key)
            progress_values.pop(key, None)
            if not active_downloads and progress:
                window.after(0, lambda: progress.set(0))
            # Обновляем лог в главном потоке:
            if lbl_log and window:
                window.after(0, lambda: lbl_log.configure(text=msg))


