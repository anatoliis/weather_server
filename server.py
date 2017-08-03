import asyncio
import sqlite3

from aiohttp import web
from jinja2 import Environment, PackageLoader, select_autoescape

from weather_controller import WeatherController
from measurement_model import db_session
from presenter import MeasurementPresenter


env = Environment(
    loader=PackageLoader('server', 'templates'),
    autoescape=select_autoescape(['html', 'xml'])
)

db_connection = sqlite3.connect('weather01.db')
weather_controller = WeatherController(db_session)


async def handle_now(request):
    template = env.get_template('info.html')
    latest_measurement = dict(await weather_controller.get_now())
    text = template.render(
        active='info',
        measurement=MeasurementPresenter(latest_measurement)
    )
    return web.Response(
        content_type='text/html',
        text=text
    )


async def handle_12_hours(request):
    template = env.get_template('12_hours.html')
    text = template.render(
        active='12_hours'
    )
    return web.Response(
        content_type='text/html',
        text=text
    )


async def handle_24_hours(request):
    template = env.get_template('24_hours.html')
    text = template.render(
        active='24_hours'
    )
    return web.Response(
        content_type='text/html',
        text=text
    )

async def init(app, loop):
    handler = app.make_handler()
    server = await loop.create_server(handler, '0.0.0.0', 80)
    print('serving on', server.sockets[0].getsockname())
    return server


if __name__ == "__main__":
    loop = asyncio.get_event_loop()

    app = web.Application(loop=loop)
    app.router.add_get('/', handle_now)
    app.router.add_get('/12_hours', handle_12_hours)
    app.router.add_get('/24_hours', handle_24_hours)
    app.router.add_static('/static/', path='./static/', name='static')

    loop.run_until_complete(init(app, loop))

    loop.run_until_complete(weather_controller.start())
    try:
        loop.run_forever()
    except:
        print('Server stopped')
