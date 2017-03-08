# coding=utf-8
from geventwebsocket import WebSocketError

from Twidder import app, database_helper, request, json, hashlib, random, string
clients = {}


@app.route("/socket")
def socket():
	if request.environ.get('wsgi.websocket'):
		ws = request.environ['wsgi.websocket']
		global clients
		while True:
			data = ws.receive()
			if data is None:
				break
			json_data = json.loads(data)
			if json_data['message'] == 'login':
				user = verify_token(json_data['token'])
				if user['email'] in clients:
					client = clients.get(user['email'])
					try:
						client.send(ResponseMessage(True, "logout").toJSON())
					except WebSocketError:
						clients.pop(user['email'])
						database_helper.remove_logged_in_user(user['email'])
				clients[user['email']] = ws
				send_chart_data()
	return '', 200


def send_chart_data():
	print("In send chart")
	global clients
	users = list()
	db_users = database_helper.find_user()

	for db_user in db_users:
		user = User()
		user.to_object(db_user)
		users.append(user)

	online_users = database_helper.get_loggedin()
	print("Online users: %i" % len(online_users))
	data = {"users": users, "online": len(online_users)}
	response = ResponseMessage(True, "chart", data)
	print(response.toJSON())
	for email, client in clients.items():
		try:
			client.send(response.toJSON())
			print("Sent data to %s" % email)
		except WebSocketError:
			clients.pop(email)
			database_helper.remove_logged_in_user(email)


@app.route('/')
def hello_world():
	return app.send_static_file('client.html')


@app.route('/login', methods=['POST'])
def sign_in():
	email = request.form['email']
	password = request.form['password']
	res = database_helper.find_user(email)
	if res is not None:
		if res['password'] == password:
			token = create_token(email)
			response = ResponseMessage(True, "Login successful", {"token": token})
		else:
			response = ResponseMessage(False, "Wrong password")
	else:
		response = ResponseMessage(False, "Wrong username")

	return response.toJSON(), 200, {'Content-type': 'application/json'}


@app.route('/logout', methods=['POST'])
def sign_out():
	token = request.args.get('token')
	token_to_user = verify_token(token)
	if token_to_user is not None:
		global clients
		email = token_to_user['email']
		clients.pop(email, None)
		database_helper.remove_token(token)
		response = ResponseMessage(True, "User logged out")
	else:
		response = ResponseMessage(False, "Not authenticated")
	send_chart_data()
	return response.toJSON(), 200, {'Content-type': 'application/json'}


@app.route('/signup', methods=['POST'])
def sign_up():
	email = request.form['email']
	password = request.form['password']
	firstname = request.form['firstname']
	familyname = request.form['familyname']
	gender = request.form['gender']
	city = request.form['city']
	country = request.form['country']

	res = database_helper.add_user(email, password, firstname, familyname, gender, city, country)

	if res is not None:
		token = create_token(email)
		response = ResponseMessage(True, 'User added', {"token": token})
	else:
		response = ResponseMessage(False, 'User already exists')
	send_chart_data()
	return response.toJSON(), 200, {'Content-Type': 'application/json'}


@app.route('/changePassword', methods=['POST'])
def change_password():
	old_password = request.form['old']
	new_password = request.form['new1']
	token = request.args.get("token")
	token_to_user = verify_token(token)
	email = token_to_user['email']
	password = token_to_user['password']
	if token_to_user is not None:
		if old_password == password:
			database_helper.update_password(email, new_password)
			response = ResponseMessage(True, "Password changed")
		else:
			response = ResponseMessage(False, "Wrong password")
	else:
		response = ResponseMessage(False, "Not authenticated")

	return response.toJSON(), 200, {'Content-Type': 'application/json'}


@app.route('/getUserData/')
def get_user_data_by_token():
	token = request.args.get("token")
	token_to_user = verify_token(token)
	email = None
	if token_to_user is not None:
		email = token_to_user['email']
	return get_user_data_by_email(email)


@app.route('/getUserData/<email>')
def get_user_data_by_email(email):
	token = request.args.get("token")
	token_to_user = verify_token(token)

	if token_to_user is not None:
		res = database_helper.find_user(email)
		if res is not None:
			user = User()
			user.to_object(res)
			response = ResponseMessage(True, "User found", user)
		else:
			response = ResponseMessage(False, "No such user")
	else:
		response = ResponseMessage(False, "Not authenticated")

	return response.toJSON(), 200, {'Content-Type': 'application/json'}


@app.route('/getUserMessages')
def get_user_messages_by_token():
	token = request.args.get("token")
	token_to_user = verify_token(token)
	email = None
	if token_to_user is not None:
		email = token_to_user['email']
	return get_user_messages_by_email(email)


@app.route('/getUserMessages/<email>')
def get_user_messages_by_email(email):
	token = request.args.get("token")
	token_to_user = verify_token(token)

	if token_to_user is not None:
		result = database_helper.get_messages(email)

		if result.__len__() > 0:
			messages = list()
			for msg in result:
				post = {"id": msg['id'], "author": msg['author'], "message": msg['message']}
				messages.append(post)

			response = ResponseMessage(True, "Messages found for user", messages)
		else:
			response = ResponseMessage(False, "No messages found for user")

	else:
		response = ResponseMessage(False, "Not authenticated")

	return response.toJSON(), 200, {'Content-Type': 'application/json'}


@app.route('/postMessage', methods=['POST'])
def post_message():
	token = request.args.get("token")
	token_to_user = verify_token(token)

	if token_to_user is not None:
		author = token_to_user['email']
		email = request.form['user']
		message = request.form['message']
		database_helper.add_message(email, author, message)
		response = ResponseMessage(True, "Message posted")
	else:
		response = ResponseMessage(False, "Not authenticated")

	return response.toJSON(), 200, {'Content-Type': 'application/json'}


@app.route('/listAllUsers', methods=['GET'])
def list_users():
	token = request.args.get("token")
	token_to_user = verify_token(token)

	if token_to_user is not None:
		users = list()
		db_users = database_helper.find_user()

		for db_user in db_users:
			users.append(db_user['email'])

		response =  ResponseMessage(True, "Users found", users)

	else:
		response = ResponseMessage(False, "Not authenticated")

	return response.toJSON(), 200, {'Content-Type': 'application/json'}


# Returns None if token is invalid
# If valid, returns the user corresponding to the token
def verify_token(token):
	res = database_helper.get_email_with_token(token)
	if res is not None:
		email = res['email']
		result = database_helper.find_user(email)
		return result
	else:
		return None


def create_token(email):
	m = hashlib.md5()
	rand = ""
	for i in range(0, 30):
		rand += random.choice(string.letters + string.digits)

	m.update(email)
	m.update(rand)

	token = m.hexdigest()
	database_helper.add_token(email, token)

	return token


class ResponseMessage:

	def __init__(self, success, message, data=None):
		self.success = success
		self.message = message
		if data is not None:
			self.data = data

	def toJSON(self):
		return json.dumps(self, default=lambda o: o.__dict__)


class User:

	def __init__(self):
		self.email = ""
		self.firstname = ""
		self.familyname = ""
		self.gender = ""
		self.city = ""
		self.country = ""

	def to_object(self, db_user):
		self.email = db_user['email']
		self.firstname = db_user['firstname']
		self.familyname = db_user['familyname']
		self.gender = db_user['gender']
		self.city = db_user['city']
		self.country = db_user['country']
