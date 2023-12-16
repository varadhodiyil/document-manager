import hashlib
import os


def generate_hash(file):
    BUF_SIZE = 65536

    sha1 = hashlib.sha1()

    f = file.open("rb")
    while True:
        data = f.read(BUF_SIZE)
        if not data:
            break
        if isinstance(data, str):
            data = data.encode()
        sha1.update(data)

    return sha1.hexdigest()


def get_upload_path(instance, filename):
    delim = "/" if "/" in instance.file.file_url else "\\"

    return os.path.join(
        # BASE_UPLOAD_PATH,
        str(instance.file.user.id),
        *(instance.file.file_url).split(delim),
        str(instance.file.current_version),
        filename,
    )
