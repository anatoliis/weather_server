import json
import asyncio
import sqlite3

from aiohttp import web
from jinja2 import Environment, PackageLoader, select_autoescape

from weather_controller import WeatherController
from measurement_model import db_session
from presenter import MeasurementPresenter, JSONMeasurementPresenter


env = Environment(
    loader=PackageLoader('server', 'templates'),
    autoescape=select_autoescape(['html', 'xml'])
)

db_connection = sqlite3.connect('weather01.db')
weather_controller = WeatherController(db_session)


async def handle_info(request):
    template = env.get_template('info.html')
    latest_measurement = await weather_controller.get_now()
    text = template.render(
        active='info',
        measurement=MeasurementPresenter(latest_measurement)
    )
    return web.Response(
        content_type='text/html',
        text=text
    )


async def handle_info_ajax(request):
    latest_measurement = await weather_controller.get_now()
    response = JSONMeasurementPresenter(latest_measurement).to_json()
    return web.Response(
        content_type='application/json',
        text=response
    )


async def handle_graph_12_h(request):
    template = env.get_template('12_hours.html')
    measurements_data = await weather_controller.get_measurements(last_hours=12)
    text = template.render(
        active='12_hours',
        json_data=json.dumps(measurements_data)
    )
    return web.Response(
        content_type='text/html',
        text=text
    )


async def handle_graph_24_h(request):
    template = env.get_template('24_hours.html')
    measurements_data = await weather_controller.get_measurements(last_hours=24)
    text = template.render(
        active='24_hours',
        json_data=json.dumps(measurements_data)
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
    app.router.add_get('/', handle_info)
    app.router.add_get('/update', handle_info_ajax)
    app.router.add_get('/12_hours', handle_graph_12_h)
    app.router.add_get('/24_hours', handle_graph_24_h)
    app.router.add_static('/static/', path='./static/', name='static')

    loop.run_until_complete(init(app, loop))

    loop.run_until_complete(weather_controller.run())
    try:
        loop.run_forever()
    except:
        print('Server stopped')
