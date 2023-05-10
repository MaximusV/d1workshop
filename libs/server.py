import asyncio
import sqlite3

from aiohttp import web

DB_NAME = "high_score.db"
GET_SQL = "SELECT rowid, name, score FROM Score WHERE name=?"
INSERT_SQL = "INSERT INTO Score (name, score) VALUES (?,?)"
UPDATE_SQL = "UPDATE Score SET score=(?) WHERE name=?"
routes = web.RouteTableDef()

@routes.get('/')
async def hello(request):
    return web.Response(text="Hello world!")

@routes.get('/user/{name}')
async def score(request):
    user_info = None
    conn = sqlite3.connect(DB_NAME)
    print(request.match_info['name'])
    with conn:
        c = conn.cursor()
        c.execute(GET_SQL, (request.match_info['name'],))
        user_info = c.fetchone()
    if user_info:
        return web.Response(text="User: {}".format(user_info))
    else:
        raise web.HTTPNotFound(body="No such user")

@routes.put('/user/{name}')
async def score(request):
    req_data = await request.json()
    name = request.match_info['name']
    score = req_data['score']
    conn = sqlite3.connect(DB_NAME)
    try:
        with conn:
            c = conn.cursor()
            c.execute(INSERT_SQL, (name,score))
    except sqlite3.IntegrityError:
        raise web.HTTPConflict(text="User: {} already exists. Use POST to update.".format(name))
    return web.Response(text="Created User: {}, score: {}".format(name, score), status=201)

@routes.post('/user/{name}')
async def score(request):
    req_data = await request.json()
    name = request.match_info['name']
    score = req_data['score']
    conn = sqlite3.connect(DB_NAME)
    try:
        with conn:
            c = conn.cursor()
            c.execute(UPDATE_SQL, (name,score))
    except sqlite3.Error as err:
        raise web.HTTPInternalServerError(text="DB error: {}".format(err))
    return web.Response(text="Updated User: {}, score: {}".format(name, score), status=200)


async def start_app():
    app = web.Application()
    app.add_routes(routes)
    # web.run_app(app)

    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, '0.0.0.0', 8080)
    await site.start()
    return runner, site


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    runner, site = loop.run_until_complete(start_app())
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        loop.run_until_complete(runner.cleanup())
