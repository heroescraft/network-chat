from flask import Flask, render_template, request
from os import listdir, remove
from os.path import isfile, join
from random import randint


#file func
def addtofile(i, a):
    with open("/home/ThbopChat/mysite/"+str(i), 'a') as f:
        f.write(str(a))

def savefile(i, a):
    with open("/home/ThbopChat/mysite/"+str(i), 'w') as f:
        f.write(str(a))

def openfile(i):
    fileread = open("/home/ThbopChat/mysite/"+str(i), 'r')
    fileread = fileread.read()
    return fileread

def getfiles(Dir):
    return [f for f in listdir("/home/ThbopChat/mysite/"+Dir) if isfile(join("/home/ThbopChat/mysite/"+Dir, f))]

def generatekey(length):
    chars='1234567890qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM'
    key = ''
    for i in range(0, length):
        key = key+str(chars[randint(0, 61)])
    return key

def debug(text):
    addtofile('debug.txt', text+'\n')

app = Flask(__name__)


#pages
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/signup.html')
def signup():
    return render_template('signup.html')

@app.route('/sus', methods=["POST"])
def sus():
    name = request.form.get("name")
    email = request.form.get("email")
    password = request.form.get("password")

    text='Hello '+name+'!'
    error=False
    url = '/'
    link='Home'

    all_emails = getfiles('accounts/')
    for aemail in all_emails:
        if email+'.data' == aemail or name == openfile('accounts/'+aemail).splitlines()[0]:
            text='Error: That account already exists!!'
            error=True

    if error == False:
        key = generatekey(randint(100, 200))
        savefile('accounts/'+email+'.data', name+'\n'+email+'\n'+password+'\n'+key+'\n0')
        url='/chat/'+key
        link='Start Chatting'



    return render_template('sus.html', text=text, url=url, link=link)

@app.route('/login.html')
def login():
    return render_template('login.html')

@app.route('/cl', methods=["POST"])
def cl():
    email = request.form.get("email")
    password = request.form.get("password")
    error=False
    found=False
    url = '/'
    link='Home'

    all_emails = getfiles('accounts/')
    for aemail in all_emails:
        if email+'.data' == aemail:
            found=True

            text='Hello '+openfile('accounts/'+aemail).splitlines()[0]+'!'

            if openfile('accounts/'+aemail).splitlines()[2] != password:
                error=True
                text='Wrong password!'
            elif openfile('accounts/'+aemail).splitlines()[2] == password:
                url='/chat/'+openfile('accounts/'+aemail).splitlines()[3]
                link='Start Chatting'

    if found == False:
        text = 'That account doesn\'t exist!'


    return render_template('cl.html', text=text, url=url, link=link)

@app.route('/chat/<key>')
def chat(key):
    accounts = getfiles('accounts/')
    error=True
    render='error.html'
    messages = 'error'

    for account in accounts:
        if key == openfile('accounts/'+account).splitlines()[3]:
            error=False
            render='chat.html'
            messages = openfile('messages.data')
            #name = openfile('accounts/'+account).splitlines()[0]



    return render_template(render, messages=messages, key=key)

@app.route('/send/<key>', methods=["POST"])
def send(key):
    message = request.form.get("message")
    accounts = getfiles('accounts/')
    names=[]
    for account in accounts:
        names.append(openfile('accounts/'+account).splitlines()[0])
        if key == openfile('accounts/'+account).splitlines()[3]:
            name = openfile('accounts/'+account).splitlines()[0]
            perms = openfile('accounts/'+account).splitlines()[4]
    if message == '/clear' and perms == '1':
        savefile('messages.data', '')

    else:
        message = name+': '+message
        addtofile('messages.data', '\n'+message)

    return render_template('send.html', key=key)


if __name__ == '__main__':
    app.run(host='0.0.0.0')
