from os import system, remove
from random import randint


chars='1234567890qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM'
key = ''
for i in range(0, randint(100, 200)):
	key = key+str(chars[randint(0, 61)])


wl = input('Are you on Windows or Linux?(w/l)\n')


if wl == 'w':
	system('color 04')
	system('cls')
else:
	system('tput setaf 5')
	system('clear')

confirm = True
print('WELCOME TO NETWORK CHAT!\nYou are this server\'s admin.')
while confirm:
	password = input('Please input your admin password:\n')
	c = input(f'"{password}" is your password right?(y/n)\n')
	if c == 'y':
		confirm = False

print(f'"{password}" is the password you will use the login to your admin account.\nThe username is "admin"\nPassword: "{password}"\nFrom now on run "app.py"')

c = input('Press ENTER to continue. ("c" to cancel)')
if c == 'c':
	if wl == 'w':
		system('cls')
		system('color 07')
	else:
		system('clear')
		system('tput setaf 7')
	quit()
	


else:
	with open('accounts.json', 'w') as f:
		f.write('{"admin":{"name":"admin","password":"'+password+'","chat_color":"red","key":"'+key+'"}}')
	
	if wl == 'w':
		system('cls')
		system('python app.py')
	else:
		system('clear')
		system('python3 app.py')
	remove('RUNME.py')
	