import asyncio
import sqlite3

from aiohttp import web

DB_NAME = "high_score.db"
GET_SQL = "SELECT rowid, name, score FROM Score WHERE name=?"

routes = web.RouteTableDef()

@routes.get('/')
async def hello(request):
    return web.Response(text="Hello, world")

@routes.get('/{name}')
async def score(request):
    user_info = None
    conn = sqlite3.connect(DB_NAME)
    print(request.match_info['name'])
    with conn:
        c = conn.cursor()
        c.execute(GET_SQL, (request.match_info['name'],))
        user_info = c.fetchone()
    return web.Response(text="User: {}".format(user_info))

#except sqlite3.IntegrityError:
#print("couldn't add Joe twice")

async def start_app():
    app = web.Application()
    app.add_routes(routes)
    # web.run_app(app)

    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, 'localhost', 8080)
    await site.start()
    return runner, site


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    runner, site = loop.run_until_complete(start_app())
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        loop.run_until_complete(runner.cleanup())
