import re 
import jwt
from datetime import datetime , timedelta  


def craft_JWT(user,key):
	payload_data = {
	"id" : user.id ,
	"username" : user.username ,
	"exp" : datetime.now() + timedelta(days=7)
	}
	return jwt.encode(payload=payload_data , key=key).decode("utf-8")

def valid_username(username) :
	return re.fullmatch("[A-Za-z0-9_-]{4,20}",username)

def valid_password(password) :
	return len(password) > 7

def valid_email(email) :
	return re.fullmatch("([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)",email)

def check_JWT(token,key):
	try :
		return jwt.decode(token, key=key, algorithms=['HS256', ])["id"]
	except Exception :
		return None
