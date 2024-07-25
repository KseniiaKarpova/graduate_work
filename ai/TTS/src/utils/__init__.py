import aiohttp
import os
from fastapi import Request

async def upload_files(file_path:str, server_url, request: Request):
    async with aiohttp.ClientSession() as session:
        data = aiohttp.FormData()
        filename = os.path.basename(file_path)
        content_type = "audio/wav"
        headers = {
            "Content-Disposition": f'attachment; filename="{filename}";',
            "Authorization": request.headers.get('Authorization'),
            "X-Request-Id": request.headers.get('X-Request-Id'),
            'X-Forwarded-For': str(request.headers.get('X-Forwarded-For'))
        }
        data.add_field(
            name="file",
            value=open(file_path, "rb"),
            filename=filename,
            content_type=content_type,
        )

        async with session.post(
            server_url,
            data=data,
            headers=headers,
            ssl=False,
        ) as response:
            status = response.status
            body = await response.json()
            return body

