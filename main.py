from sanic import Sanic, response
from sanic_auth import Auth, User
from sanic.response import json
from sanic_session import Session
from sanic_session import InMemorySessionInterface
from sanic_jinja2 import SanicJinja2

from databases import Database
# database = Database('mysql://')
app = Sanic(__name__)

app.config.AUTH_LOGIN_ENDPOINT = 'login'

app.config.DB_NAME = 'appdb'
app.config.DB_HOST = 'localhost',
app.config.DB_USER = 'daulet'
# Session(app)
app.static('/static', './static')

jinja = SanicJinja2(app)
session = InMemorySessionInterface(cookie_name=app.name, prefix=app.name)
auth = Auth(app)


@app.middleware("request")
async def add_session_to_request(request):
	# before each request initialize a session
	# using the client's request
	await session.open(request)


@app.middleware("response")
async def save_session(request, response):
	# after each request save the session,
	# pass the response to set client cookies
	await session.save(request, response)


@app.route("/")
@jinja.template('index.html')
async def index(request):
	return jinja.render("index.html", request, greetings="Hello, sanic!")



@app.route("/about")
async def about(request):
	return jinja.render("about.html", request)


# LOGIN_FORM = '''
# <h2>Please sign in, you can try:</h2>
# <dl>
# <dt>Username</dt> <dd>demo</dd>
# <dt>Password</dt> <dd>1234</dd>
# </dl>
# <p>{}</p>
# <form action="" method="POST">
#   <input class="username" id="name" name="username"
# 	placeholder="username" type="text" value=""><br>
#   <input class="password" id="password" name="password"
# 	placeholder="password" type="password" value=""><br>
#   <input id="submit" name="submit" type="submit" value="Sign In">
# </form>
# '''
#
#
# @app.route('/login', methods=['GET', 'POST'])
# async def login(request):
# 	message = ''
# 	if request.method == 'POST':
# 		username = request.form.get('username')
# 		password = request.form.get('password')
# 		# fetch user from database
# 		# user = some_datastore.get(name=username)
# 		user = User(id = 1, name = username)
# 		if user and user.check_password(password):
# 			auth.login_user(request, user)
# 			return response.redirect('/profile')
# 		return response.html(LOGIN_FORM.format(message))
#
#
# @app.route('/logout')
# @auth.login_required
# async def logout(request):
# 	auth.logout_user(request)
# 	return response.redirect('/login')
#
#
# @app.route('/profile')
# @auth.login_required(user_keyword='user')
# async def profile(request, user):
# 	return response.json({'user': user})


if __name__ == "__main__":
	app.run(host="127.0.0.1", port=8000, debug=True)