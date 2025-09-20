import os
from aiohttp import web


LOCAL_DIR = './'


async def handle_get_file(request):
    rel_path = request.match_info.get('path', '')
    full_path = os.path.join(LOCAL_DIR, rel_path)

    if not os.path.exists(full_path) or not os.path.isfile(full_path):
        return web.Response(text="File not found", status=404)

    return web.FileResponse(full_path)

app = web.Application()
app.add_routes([
    web.get('/{path:.*}', handle_get_file)
])

if __name__ == '__main__':
    web.run_app(app, host='127.0.0.1', port=1488)