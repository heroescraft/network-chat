from flask import Flask, render_template, request
import json
from random import randint



def openfile(a):
	return open(a, 'r').read()

def savefile(a, b):
	with open(a, 'w') as f:
		f.write(b)

def generatekey(length):
    chars='1234567890qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM'
    key = ''
    for i in range(0, length):
        key = key+str(chars[randint(0, 61)])
    return key

def makeAccount(name, password):
	accounts = json.loads(openfile('accounts.json'))
	key = generatekey(randint(100, 400))
	accounts[name] = {"name":name,"password":password,"chat_color":"amber","key":key}
	savefile('accounts.json', json.dumps(accounts))

def getAccount(name, key='', fromkey=False):
	accounts = json.loads(openfile('accounts.json'))
	if not fromkey:
		return accounts[name]
	else:
		for account in accounts.keys():
			if accounts[account]['key'] == key:
				return accounts[account]

def sendMessage(key, message):
	sender = getAccount('', key, True)
	send_message = True
	
	if sender['name'] == 'admin':
		send_message = False
		if message == '/clear':
			savefile('messages.json', json.dumps([{"name":"SERVER","message":"Welcome!","color":"blue"}]))
			
		
		
		else:
			send_message = True
			
	if send_message:
		messages = json.loads(openfile('messages.json'))
		messages.append({"name":sender['name'],"message":message,"color":sender['chat_color']})
		savefile('messages.json', json.dumps(messages))
	



app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/signup')
def signup():
	return render_template('signup.html', name='', password='', key='')

@app.route('/signup_process', methods=['POST'])
def signup_process():
	name = request.form.get('name')
	password = request.form.get('password')
	error = True
	error_message = 'Error!'
	key = ''

	
	accounts = json.loads(openfile('accounts.json'))
	for username in accounts.keys():
		if name.lower() != username.lower():
			error = False
		else: 
			error = True
			error_message = 'That username is taken!'
	if not error:
		if password == '':
			error = True
			error_message = '"" isn\'t a password!'
		if name == '':
			error = True
			error_message = '"" isn\'t a name!'
		if not error:
			makeAccount(name, password)
			key = getAccount(name)['key']
			
	return render_template('signup.html', 
	error=error, 
	error_message=error_message,
	name=name,
	password=password,
	key=key)	

@app.route('/login')
def login():
	return render_template('login.html', name='', password='', key='')
		
@app.route('/login_process', methods=['POST'])
def login_process():
	name = request.form.get('name')
	password = request.form.get('password')
	error = True
	error_message = 'Wrong username!'
	key=''
	
	accounts = json.loads(openfile('accounts.json'))
	for username in accounts.keys():
		if name == username:
			if password == getAccount(name)['password']:
				error = False
				key=getAccount(name)['key']
			else:
				error = True
				error_message = 'Wrong password!'
			
	return render_template('login.html', 
	error=error, 
	error_message=error_message,
	name=name,
	password=password,
	key=key)	
	
@app.route('/chat<key>')
def chat(key):
	return render_template('chat.html',
	messages=json.loads(openfile('messages.json')),
	key=key)
	
@app.route('/send<key>', methods=['POST'])
def send(key):
	message = request.form.get('message')
	
	sendMessage(key, message)
	
	
	return render_template('process.html',
	url=f'/chat{key}#bottom')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
