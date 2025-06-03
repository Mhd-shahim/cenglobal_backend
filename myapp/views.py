import paramiko
from django.http import StreamingHttpResponse
from django.http import JsonResponse


SFTP_HOST = 'localhost' 
SFTP_PORT = 22
SFTP_USER = 'sftpuser'
SFTP_PASS = '123456'



def stream_video(request, filename):
    remote_path = f"/uploads/{filename}"  # Dynamically construct the file path
    transport = paramiko.Transport((SFTP_HOST, SFTP_PORT))
    transport.connect(username=SFTP_USER, password=SFTP_PASS)
    sftp = paramiko.SFTPClient.from_transport(transport)
    remote_file = sftp.open(remote_path, 'rb')

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


def list_files(request):
    try:
        # Connect to the SFTP server
        transport = paramiko.Transport((SFTP_HOST, SFTP_PORT))
        transport.connect(username=SFTP_USER, password=SFTP_PASS)
        sftp = paramiko.SFTPClient.from_transport(transport)

        # List files in the uploads folder
        uploads_path = "/uploads/"
        files = sftp.listdir(uploads_path)

        # Return the list of files as a JSON response
        return JsonResponse({"files": files}, status=200)

    except Exception as e:
        # Handle errors and return a response
        return JsonResponse({"error": str(e)}, status=500)

    finally:
        # Ensure the SFTP connection is closed
        if sftp:
            sftp.close()
        if transport:
            transport.close()