import paramiko
from django.http import StreamingHttpResponse

SFTP_HOST = 'sftp://localhost' 
SFTP_PORT = 22
SFTP_USER = 'sftpuser'
SFTP_PASS = '123456'
REMOTE_PATH = '/uploads/SampleVideo_1280x720_30mb.mp4'

def sftp_stream():
    transport = paramiko.Transport((SFTP_HOST, SFTP_PORT))
    transport.connect(username=SFTP_USER, password=SFTP_PASS)
    sftp = paramiko.SFTPClient.from_transport(transport)
    remote_file = sftp.open(REMOTE_PATH, 'rb')
    return remote_file, transport, sftp

def stream_video(request):
    remote_file, transport, sftp = sftp_stream()

    def file_iterator(file, chunk_size=8192):
        try:
            while True:
                data = file.read(chunk_size)
                if not data:
                    break
                yield data
        finally:
            file.close()
            sftp.close()
            transport.close()

    return StreamingHttpResponse(file_iterator(remote_file), content_type='video/mp4')