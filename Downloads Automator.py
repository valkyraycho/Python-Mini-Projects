import os
import shutil

image_extensions = [".jpg", ".jpeg", ".jpe", ".jif", ".jfif", ".jfi", ".png", ".gif", ".webp", ".tiff", ".tif", ".psd", ".raw", ".arw", ".cr2", ".nrw",
                    ".k25", ".bmp", ".dib", ".heif", ".heic", ".ind", ".indd", ".indt", ".jp2", ".j2k", ".jpf", ".jpf", ".jpx", ".jpm", ".mj2", ".svg", ".svgz", ".ai", ".eps", ".ico"]

video_extensions = [".webm", ".mpg", ".mp2", ".mpeg", ".mpe", ".mpv", ".ogg",
                    ".mp4", ".mp4v", ".m4v", ".avi", ".wmv", ".mov", ".qt", ".flv", ".swf", ".avchd"]

audio_extensions = [".m4a", ".flac", "mp3", ".wav", ".wma", ".aac"]

word_extensions = [".doc", ".docx", ".odt"]

pdf_extension = [".pdf"]

excel_extension = [".xls", ".xlsx", ".csv"]

ppt_extension = [".ppt", ".pptx"]

compressed_folder_extensions = [".zip", ".tar", ".tar.gz", ".tar.bz2", ".tar.xz",
                                ".7z", ".rar", ".gz", ".bz2", ".xz", ".z", ".tgz", ".tbz2", ".txz", ".sitx", ".cab"]


source_dir = r"C:\Users\razor\Downloads"
dest_dir_music = r"C:\Users\razor\Downloads\Music"
dest_dir_video = r"C:\Users\razor\Downloads\Video"
dest_dir_image = r"C:\Users\razor\Downloads\Image"
dest_dir_word = r"C:\Users\razor\Downloads\Word"
dest_dir_pdf = r"C:\Users\razor\Downloads\PDF"
dest_dir_excel = r"C:\Users\razor\Downloads\Excel"
dest_dir_ppt = r"C:\Users\razor\Downloads\PPT"
dest_dir_folder = r"C:\Users\razor\Downloads\Folder"
dest_dir_compressed = r"C:\Users\razor\Downloads\Compressed"
dest_dir_other = r"C:\Users\razor\Downloads\Other"


files = {
    'image': {
        'extension': image_extensions,
        'destination': dest_dir_image
    },
    'music': {
        'extension': audio_extensions,
        'destination': dest_dir_music
    },
    'video': {
        'extension': video_extensions,
        'destination': dest_dir_video
    },
    'word': {
        'extension': word_extensions,
        'destination': dest_dir_word
    },
    'pdf': {
        'extension': pdf_extension,
        'destination': dest_dir_pdf
    },
    'excel': {
        'extension': excel_extension,
        'destination': dest_dir_excel
    },
    'ppt': {
        'extension': ppt_extension,
        'destination': dest_dir_ppt
    },
    'compressed_folder': {
        'extension': compressed_folder_extensions,
        'destination': dest_dir_compressed
    }
}

folders = ['Image', 'Music', 'Video', 'Word', 'PDF', 'Excel', 'PPT', 'Other', 'Folder', 'Compressed']

def make_unique(dest, name):
    filename, extension = os.path.splitext(name)
    counter = 1
    while os.path.exists(f'{dest}\{name}'):
        name = f"{filename}-{str(counter)}{extension}"
        counter += 1
    return name

def move_file(source, dest, name):
    if os.path.exists(f"{dest}\{name}"):
        unique_name = make_unique(dest, name)
        old_name = os.path.join(dest, name)
        new_name = os.path.join(dest, unique_name)
        os.rename(old_name, new_name)
    shutil.move(source, dest)

with os.scandir(source_dir) as entries:
    for entry in entries:
        source = f"{source_dir}\{entry.name}"

        if entry.is_dir() and entry.name in folders:
            pass
            
        elif entry.is_dir():
            destination = dest_dir_folder
            shutil.move(source, destination)
            
        else:
            extension = "."+entry.name.split('.')[-1].lower()
            for file in files:
                if extension in files[file]['extension']:
                    destination = files[file]['destination']
                    source = f"{source_dir}\{entry.name}"
                    move_file(source, destination, entry.name)
                    break
            else:
                source = f"{source_dir}\{entry.name}"
                destination = dest_dir_other
                move_file(source, destination, entry.name)


