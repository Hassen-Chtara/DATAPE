from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.config['SECRET_KEY'] = 'ad65apyojt5a6e5dz68a8ac561a3d79wgljy'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
jwtkey='ABA6867C1FD6646EA2879F9AFBA2648EE2231D7B8E25B13137'

from DATAPE import routes