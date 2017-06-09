from flask import Flask, session, redirect, url_for, escape, request
import requests
import json
from models import SisResumo, SisLanc
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
from config import SERVER_ADDR


app = Flask(__name__)
API_KEY = '83fdf5e05ffb52a01f37c22b27e0da07'

app_settings = os.getenv(
    'APP_SETTINGS',
    'config.DevelopmentConfig'
)
app.config.from_object(app_settings)
db = SQLAlchemy(app)


def mk_login(username, passwd):
    resp = requests.get('http://api:'+API_KEY+'@'+SERVER_ADDR+'/api/cliente/list/'+username)
    if resp.status_code == 200:
        json_data = resp.json()
        if json_data == 'NULL':
            return False
        if json_data['dados'][0]['senha'] == passwd:
            return True
    return False


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        logout()
    if 'username' not in session:
        return 'You are not logged in'
    return '''
        Logged in as %s
    <form method="post">
        <p><input type=submit value=Logout>
    </form>
    ''' % escape(session['username'])


@app.route('/titulos')
def titulos():
    if 'username' not in session:
        return 'You are not logged in'
    t_list = db_session.query(SisLanc).filter(SisLanc.login == session['username']).all()
    for itm in t_list:
        print(itm.valor)
    req = requests.get('http://192.168.1.200/api/83fdf5e05ffb52a01f37c22b27e0da07/titulo/list')
    if req.status_code != 200:
        return 'Error: mk-auth internal server error!'
    resp = req.json()
    if resp == 'NULL':
        return 'Error: content not found!'
    bill_list = []
    for item in resp['titulos']:
        if item['login'] == session['username']:
            bill_list.append(item)
    json_ret = json.dumps(bill_list)
    return json_ret


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if mk_login(request.form['username'], request.form['password']):
            session['username'] = request.form['username']
            return redirect(url_for('index'))
        return redirect(url_for('login'))
    return '''
        <form method="post">
            <p><input type=text name=username>
            <p><input type=password name=password>
            <p><input type=submit value=Login>
        </form>
    '''


@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('username', None)
    return redirect(url_for('index'))

# set the secret key.  keep this really secret:
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
app.debug = True

if __name__ == '__main__':
    engine = create_engine("mysql://root:vertrigo@"+SERVER_ADDR+"/mkradius")
    Session = sessionmaker(bind=engine)
    db_session = Session()
    app.run()

# TODO: Ajustar os retornos das páginas para formato JSON
# TODO: Trocar a key dos cookies
# TODO: Trocar login via form para JSON
# TODO: Utilizar JWT para todo o conteúdo JSON
