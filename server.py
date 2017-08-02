import asyncio
from aiohttp import web
from jinja2 import Template, Environment, PackageLoader, select_autoescape


loop = asyncio.get_event_loop()


env = Environment(
	loader=PackageLoader('server', 'templates'),
	autoescape=select_autoescape(['html', 'xml'])
)


async def handle_now(request):
	template = env.get_template('info.html')
	text = template.render(
		active='info'
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


app = web.Application(loop=loop)
app.router.add_get('/', handle_now)
app.router.add_get('/12_hours', handle_12_hours)
app.router.add_get('/24_hours', handle_24_hours)
app.router.add_static('/static/', path='./static/', name='static')

web.run_app(app, port=80)

#TODOS
# 2. Add some bootstrap template
# 3. Create 3 tabs
# 4. No JS tabs only get requests, no autoupdate
# 5. Background worker, saving info to RAM
# 6. Getting info from RAM on request
# 7. Saving info to DB each minute
# 8. Split db files by size (100 mb, 10 kb for testing)
# 9. Tab with db size information
# 10. Creating and downloading db archive
