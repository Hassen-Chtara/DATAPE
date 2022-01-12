from  flask import request , render_template ,redirect ,url_for ,make_response
from DATAPE import app , db , bcrypt , jwtkey
from DATAPE.models import *
from DATAPE.functions import *
import base64
 

@app.route('/home')
@app.route('/' , methods=["GET"])
def home():
	return render_template("home.html",cookie=check_JWT(request.cookies.get("session"),jwtkey),css='home.css',name="home")


@app.route('/login' , methods=["GET","POST"])
def login():
	if request.method == 'POST' :
		username=request.form.get("username")
		password=request.form.get("password")
		if username==None or password==None :
			return "Bad Request" , 400
		user=User.query.filter_by(username=username).first()
		if user and bcrypt.check_password_hash(user.password, password):
			response = make_response(redirect('data'))
			response.set_cookie('session', craft_JWT(user,jwtkey))
			return response
		return "invalid username or password"
	if check_JWT(request.cookies.get("session"),jwtkey) :
		redirect(url_for("home"))
	return render_template("login.html",name="login")



@app.route('/signup' , methods=["GET","POST"])
def signup():
	if request.method == 'POST' :
		username=request.form.get("username")
		password=request.form.get("password")
		email=request.form.get("email")
		if username==None or password==None or email==None :
			return "Bad Request" , 400
		user=User.query.filter_by(username=username).first()
		if user :
			return "username already taken" , 400
		user=User.query.filter_by(email=email).first()
		if user :
			return "email already taken", 400
		hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
		db.session.add(User(username=username,password=hashed_password,email=email))
		db.session.commit()
		return redirect(url_for("login"),code=302)
	if check_JWT(request.cookies.get("session"),jwtkey) :
		redirect(url_for("home"))
	return render_template("signup.html",cookie=check_JWT(request.cookies.get("session"),jwtkey),name="signup")


@app.route("/logout")
def logout():
	response = make_response(redirect('login'))
	response.set_cookie('session', '' , expires=0)
	return response


@app.route('/data' , methods=["GET"])
def data():
	user_id=check_JWT(request.cookies.get("session"),jwtkey)
	if user_id :
		domains = {i:Data.query.filter_by(domain_id=i.id).all() for i in Domain.query.filter_by(user_id=user_id).all()}
		return render_template("mydata.html" , cookie=user_id ,name="data", css='mydata.css',Domains=domains)
	return "Forbidden" , 403


@app.route('/profile' , methods=["GET","POST"])
def profile():
	user_id=check_JWT(request.cookies.get("session"),jwtkey)
	if not user_id :
		return "Forbidden" , 403

	if request.method == 'POST' :
		domain=request.form.get("domain")
		db.session.add(Domain(name=domain,ip=domain,user_id=user_id))
		db.session.commit()
	return render_template("profile.html" , cookie=user_id ,name="profile", css='profile.css',domains=[(i.name,"http://DATAPE.com/api/"+base64.b64encode(str(i.id).encode()).decode("ascii").replace("=","")) for i in Domain.query.filter_by(user_id=user_id).all()])
	
@app.route("/api/<Domain64>" , methods=["POST"])
def api(Domain64):
	Domain64 += '='* (4 - len(Domain64)%4)
	domain=base64.b64decode(Domain64.encode("ascii")).decode("ascii")
	content_type = request.headers.get('Content-Type')
	if ( 'application/json' in content_type ):
		db.session.add(Data(domain_id=domain,content=str(request.json)))
		db.session.commit()
	return "" , 200
