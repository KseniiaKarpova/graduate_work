from fastapi import UploadFile
from exceptions import big_file, file_error


class Detector:

    async def check_file(self, upload_file: UploadFile):
        if upload_file.size > 300500:
            raise big_file

        if upload_file.content_type != 'audio/wav' and upload_file.content_type != 'audio/x-wav':
            raise file_error


def get_detector() -> Detector:
    return Detector()
