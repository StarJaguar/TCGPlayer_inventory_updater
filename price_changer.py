from flask import Flask, render_template, request, redirect, url_for, flash, abort, send_file
from werkzeug.utils import secure_filename, safe_join
import os
import datetime as dt
from market_adjuster import price_changer
from pathlib import Path

ALLOWED_EXTENSIONS = {'.csv'}

app = Flask(__name__)

FolderPath = 'C:/Users/Taylor/Documents/Projects/GIt_repositories/TCGPlayer_inventory_updater/static/datasets'

@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template('file_upload.html')

@app.route('/upload-file', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':

        f=request.files['file']
        if f.filename != '':
            file_ext = os.path.splitext(f.filename)[1]
            if file_ext not in ALLOWED_EXTENSIONS:
                abort(400)

            upload_time = dt.datetime.now().strftime("_%Y_%m_%d")
            full_name = secure_filename(os.path.splitext(f.filename)[0]) + upload_time + '.csv'
            f.save('C:/Users/Taylor/Documents/Projects/GIt_repositories/TCGPlayer_inventory_updater/static/datasets/' + full_name)
            price_changer(full_name)

        else:
            flash('No file selected.')
            return redirect(url_for('home'))

    return redirect(url_for(('home')))

def getReadableByteSize(num, suffix='B') -> str:
    for unit in ['', 'K', 'M', 'G', 'T', 'P', 'E', 'Z']:
        if abs(num) < 1024.0:
            return "%3.1f%s%s" % (num, unit, suffix)
        num /= 1024.0
    return "%.1f%s%s" % (num, 'Yi', suffix)

def getTimeStampString(tSec: float) -> str:
    tObj = dt.datetime.fromtimestamp(tSec)
    tStr = dt.datetime.strftime(tObj, '%Y-%m-%d %H:%M:%S')
    return tStr

def getIconClassForFilename(fName):
    fileExt = Path(fName).suffix
    fileExt = fileExt[1:] if fileExt.startswith(".") else fileExt
    fileTypes = ["aac", "ai", "bmp", "cs", "css", "csv", "doc", "docx", "exe", "gif", "heic", "html", "java", "jpg", "js", "json", "jsx", "key", "m4p", "md", "mdx", "mov", "mp3",
                 "mp4", "otf", "pdf", "php", "png", "pptx", "psd", "py", "raw", "rb", "sass", "scss", "sh", "sql", "svg", "tiff", "tsx", "ttf", "txt", "wav", "woff", "xlsx", "xml", "yml"]
    fileIconClass = f"bi bi-filetype-{fileExt}" if fileExt in fileTypes else "bi bi-file-earmark"
    return fileIconClass

@app.route('/reports/', defaults={'reqPath': ''})
@app.route('/reports/<path:reqPath>')
def getFiles(reqPath):
    # Join the base and the requested path
    # could have done os.path.join, but safe_join ensures that files are not fetched from parent folders of the base folder
    absPath = safe_join(FolderPath, reqPath)

    # Return 404 if path doesn't exist
    if not os.path.exists(absPath):
        return abort(404)

    # Check if path is a file and serve
    if os.path.isfile(absPath):
        return send_file(absPath)

    # Show directory contents
    def fObjFromScan(x):
        fileStat = x.stat()
        # return file information for rendering
        return {
                'name': x.name,
                'fIcon': "bi bi-folder-fill" if os.path.isdir(x.path) else getIconClassForFilename(x.name),
                'relPath': os.path.relpath(x.path, FolderPath).replace("\\", "/"),
                'mTime': getTimeStampString(fileStat.st_mtime),
                'size': getReadableByteSize(fileStat.st_size)
               }
    
    fileObjs = [fObjFromScan(x) for x in os.scandir(absPath)]
    # get parent directory url
    parentFolderPath = os.path.relpath(Path(absPath).parents[0], FolderPath).replace("\\", "/")

    return render_template('files.html.j2', data={'files': fileObjs, 'parentFolder': parentFolderPath})