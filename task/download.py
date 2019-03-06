import os
import shutil
from hashlib import md5
from model.db_model import Session, OfflineDownload, File, FileType
from .celery import app
from utils.aria2 import Aria2
from utils.filetype import check_file_type
from config import ARIA2_HOST, ARIA2_PORT, ARIA2_TOKEN, FILE_PATH, SPLIT_SIZE

MAX_READ_SIZE = SPLIT_SIZE * 10
aria2 = Aria2(ARIA2_HOST, ARIA2_PORT, ARIA2_TOKEN)


def _addUri(id, uris):
    if len(uris) > 1:
        raise ValueError("uris only support one uri.")
    r = aria2.addUri(uris)
    print(r)

    session = Session()
    if 'error' in r:
        error_code = r['error']['code']
        error_message = r['error']['message']
        done = True
        session.query(OfflineDownload).filter(OfflineDownload.id == id).update({
            'error': error_code,
            'message': error_message,
            'done': done
        })
    else:
        gid = r['result']
        session.query(OfflineDownload).filter(
            OfflineDownload.id == id).update({'gid': gid})
    session.commit()

    return r


def add_new_file(id, file_path):
    session = Session()
    download_file = session.query(OfflineDownload).filter(OfflineDownload.id == id).first()
    userid = download_file.userid
    filename = download_file.filename
    uploaddate = download_file.time
    # path = download_file.path
    filesize = os.path.getsize(file_path)
    # find the file and calculate the md5.
    with open(file_path, 'rb') as f:
        m = md5()
        r = f.read(MAX_READ_SIZE)
        m.update(r)
        while len(r) > 0:
            r = f.read(MAX_READ_SIZE)
            m.update(r)
        md5_str = m.hexdigest()
    filetype = session.query(FileType).filter(FileType.filetype == check_file_type(filename)).first()
    if not filetype:
        raise TypeError('can not specify filetype for {}'.format(filename))
    filetype = filetype.id
    file = File(
        userid=userid,
        filetype=filetype,
        filename=filename,
        filesize=filesize,
        uploaddate=uploaddate,
        path=download_file.path,
        md5=md5_str
    )
    session.add(file)
    session.commit()
    # move the file to destination dir
    new_path = FILE_PATH + os.sep + md5_str
    shutil.move(file_path, new_path)


def _refresh():
    session = Session()
    downloads = session.query(OfflineDownload).filter(OfflineDownload.done == False).all()  # noqa
    for d in downloads:
        r = aria2.getFiles(d.gid)
        if 'error' in r:
            error_code = r['error']['code']
            error_message = r['error']['message']
            d.code = error_code
            d.message = error_message
            d.done = True
            continue
        result = r['result'][0]
        total_length = result['length']
        completed = int(float(result['completedLength']) / float(total_length) * 100)
        done = (completed == 100)
        path = result['path']
        filename = os.path.split(path)[-1] if (d.filename is None) else None
        session.query(OfflineDownload).filter(OfflineDownload.id == d.id).update({
            'filename': filename,
            'path': d.path,  # this path is virtual path for cloudr
            'completed': completed,
            'done': done
        })
        # if done move the file into file dir, and insert a row into File
        done and add_new_file(d.id, path)
    session.commit()


@app.task
def addUri(id, uris):
    return _addUri(id, uris)


@app.task
def refresh():
    # todo: when some files download error, they need to be removed from aria2 and delete files.
    _refresh()
