import asyncio
import json

from aiohttp import web
from jinja2 import Environment, PackageLoader, select_autoescape

from helpers import get_hours
from measurement import db_session
from weather_controller import WeatherController

env = Environment(
    loader=PackageLoader('server', 'templates'),
    autoescape=select_autoescape(['html', 'xml'])
)

weather_controller = WeatherController(db_session)


async def handle_info(request):
    template = env.get_template('info.html')
    latest_measurement = await weather_controller.get_latest_measurement()
    text = template.render(
        active='info',
        measurement=latest_measurement.to_dict()
    )
    return web.Response(
        content_type='text/html',
        text=text
    )


async def handle_info_ajax(request):
    measurement = await weather_controller.get_latest_measurement()
    return web.Response(
        content_type='application/json',
        text=measurement.to_json()
    )


async def handle_chart(request):
    hours = get_hours(request.rel_url.query)
    template = env.get_template('chart.html')
    measurements = await weather_controller.get_measurements(last_hours=hours)
    measurements = tuple(map(lambda m: m.to_dict(), measurements))
    text = template.render(
        active='%s_hours' % hours,
        json_data=json.dumps(measurements)
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
    app.router.add_get('/chart', handle_chart)
    app.router.add_static('/static/', path='./static/', name='static')

    loop.run_until_complete(init(app, loop))

    loop.run_until_complete(weather_controller.run())
    try:
        loop.run_forever()
    except:
        print('Server stopped')
