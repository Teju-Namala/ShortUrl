import os
from flask import Flask,render_template,request,redirect,session,url_for
from flask_sqlalchemy import SQLAlchemy
import string,random

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] =\
        'sqlite:///' + os.path.join(basedir, 'database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Urls(db.Model):
    id = db.Column("id",db.Integer, primary_key=True)
    long = db.Column("long",db.String())
    short = db.Column("short",db.String(5))

    def __init__(self,long,short):
        self.long=long
        self.short=short
    
@app.before_first_request
def create_table():
    db.create_all()

def shorten_url():
    letters= string.ascii_lowercase +string.ascii_uppercase
    while True:
        rand_letters=random.choices(letters,k=3)
        rand_letters="".join(rand_letters)
        shortUrl=Urls.query.filter_by(short=rand_letters).first()
        if not shortUrl:
            return rand_letters

@app.route("/home",methods=['POST','GET'])
def home():
    if request.method=='POST':
        receiveUrl=request.form['lurl']
        #if exists
        foundUrl=Urls.query.filter_by(long=receiveUrl).first()
        if foundUrl:
            return redirect(url_for("displayShortUrl",url=foundUrl.short))
        else:
            #not exists -> create
            shortUrl=shorten_url()
            newUrl=Urls(receiveUrl,shortUrl)
            db.session.add(newUrl)
            db.session.commit()
            return redirect(url_for("displayShortUrl",url=shortUrl))
    else:
        return render_template('home.html')


@app.route('/display/<url>')
def displayShortUrl(url):
    return render_template('base.html',displayShort=url)

@app.route('/<shortUrl>')
def redirection(shortUrl):
    LongUrl=Urls.query.filter_by(short=shortUrl).first()
    if LongUrl:
        return redirect(LongUrl.long)
    else:
        return f'<h2>URl doesnt exist</h2>'

app.run()








#classname.query.filterby().first() 