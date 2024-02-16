from . node import *

import server
from aiohttp import web
import shutil
import os

@server.PromptServer.instance.routes.post("/tx/batch-download")
async def download_files_by_path(request):
    # TODO: replace '/path/to/your/folder' with your folder path
    # 获取当前文件的绝对路径
    curr_file_path = os.path.abspath(__file__)
    print(f"Current file path: {curr_file_path}")

    # 使用os.path.dirname获取当前文件的上级目录
    parent_dir = os.path.dirname(curr_file_path)
    print(f"Parent directory: {parent_dir}")
    
    folder_path = os.path.join(parent_dir, 'output')

    # Compress the folder
    shutil.make_archive('archive_name', 'zip', folder_path)
    
    resp = web.StreamResponse(
        headers={
            'CONTENT-DISPOSITION': 'attachment; filename="archive_name.zip"'
        }
    )

    # Open the file in binary mode and stream it to the response
    file_path = 'archive_name.zip'
    file_size = os.path.getsize(file_path)

    resp.content_length = file_size
    resp.content_type = 'application/zip'

    await resp.prepare(request)
    with open(file_path, 'rb') as file:
        chunk = file.read(8196)
        while chunk:
            await resp.write(chunk)
            chunk = file.read(8196)

    return resp

WEB_DIRECTORY  = 'js'

__all__ = ["NODE_CLASS_MAPPINGS","NODE_DISPLAY_NAME_MAPPINGS"]