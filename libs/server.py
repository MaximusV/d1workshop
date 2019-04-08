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

app = web.Application()
app.add_routes(routes)
web.run_app(app)
