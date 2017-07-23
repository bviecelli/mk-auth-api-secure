from flask import Flask, session, redirect, url_for, escape, request
import jwt
import json
from models import SisResumo, SisLanc, SisCliente, SisMsg, SisSuporte
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
from config import SERVER_ADDR
from decimal import Decimal


app = Flask(__name__)
JWT_KEY = 'secret_test'

app_settings = os.getenv(
    'APP_SETTINGS',
    'config.DevelopmentConfig'
)
app.config.from_object(app_settings)
db = SQLAlchemy(app)


def encapsulate_jwt(pkt):
    if USE_JWT:
        data = jwt.encode({"data": pkt}, JWT_KEY, algorithm='HS256').decode()
    else:
        data = pkt
    return data


def ret_error(err):
    data = {"error": err}
    return encapsulate_jwt(data)


def mk_login(username, passwd):
    t_list = db_session.query(SisCliente).filter(SisCliente.login == username).all()
    if t_list.__len__ == 0:
        return False
    if t_list[0].senha == passwd:
        return True
    return False
    # resp = requests.get('http://api:'+API_KEY+'@'+SERVER_ADDR+'/api/cliente/list/'+username)
    # if resp.status_code == 200:
    #     json_data = resp.json()
    #     if json_data == 'NULL':
    #         return False
    #     if json_data['dados'][0]['senha'] == passwd:
    #         return True
    # return False


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        logout()
    if 'username' not in session:
        return ret_error('You are not logged in')
    data = json.dumps({"result": "success", "user": session['username']}, ensure_ascii=False)
    return encapsulate_jwt(data)


@app.route('/titulos')
def titulos():
    if 'username' not in session:
        return ret_error('You are not logged in')
    t_list = db_session.query(SisLanc).filter(SisLanc.login == session['username']).all()

    bill_list = []
    for itm in t_list:
        lst = vars(itm).copy()
        lst.__delitem__('_sa_instance_state')
        bill_list.append(lst)
    json_ret = json.dumps(bill_list, ensure_ascii=False, default=default)
    return encapsulate_jwt(json_ret)


def default(obj):
    if isinstance(obj, Decimal):
        return str(obj)


@app.route('/conta')
def conta():
    if 'username' not in session:
        return ret_error('You are not logged in')
    t_list = db_session.query(SisCliente).filter(SisCliente.login == session['username']).first()

    lst = vars(t_list).copy()
    lst.__delitem__('_sa_instance_state')
    lst.__delitem__('senha')
    c_list = json.dumps(lst, ensure_ascii=False, default=default)
    return encapsulate_jwt(c_list)


@app.route('/resumo')
def resumo():
    if 'username' not in session:
        return ret_error('You are not logged in')
    t_list = db_session.query(SisResumo).filter(SisResumo.login == session['username']).all()

    c_list = []
    for itm in t_list:
        lst = vars(itm).copy()
        lst.__delitem__('_sa_instance_state')
        c_list.append(lst)
    json_ret = json.dumps(c_list, ensure_ascii=False, default=default)
    return encapsulate_jwt(json_ret)


@app.route('/msgs')
def msgs():
    if 'username' not in session:
        return ret_error('You are not logged in')
    t_list = db_session.query(SisMsg).filter(SisMsg.login == session['username']).all()

    c_list = []
    for itm in t_list:
        lst = vars(itm).copy()
        lst.__delitem__('_sa_instance_state')
        c_list.append(lst)
    json_ret = json.dumps(c_list, ensure_ascii=False, default=default)
    return encapsulate_jwt(json_ret)


@app.route('/chamados')
def chamados():
    if 'username' not in session:
        return ret_error('You are not logged in')
    t_list = db_session.query(SisSuporte).filter(SisSuporte.login == session['username']).all()

    c_list = []
    for itm in t_list:
        lst = vars(itm).copy()
        lst.__delitem__('_sa_instance_state')
        c_list.append(lst)
    json_ret = json.dumps(c_list, ensure_ascii=False, default=default)
    return encapsulate_jwt(json_ret)


@app.route('/login', methods=['POST'])
def login():
    if len(request.form['data']) > 0:
        if USE_JWT:
            data = jwt.decode(request.form['data'], JWT_KEY, algorithm='HS256')
        else:
            data = json.loads(request.form['data'])
        if mk_login(data['username'], data['password']):
            session['username'] = data['username']
            return encapsulate_jwt(json.dumps({"result": "success", "user": session['username']}, ensure_ascii=False))
    return ret_error('You are not logged in')


@app.route('/login_test', methods=['GET', 'POST'])
def login_test():
    if request.method == 'POST':
        if mk_login(request.form['username'], request.form['password']):
            session['username'] = request.form['username']
            return encapsulate_jwt(json.dumps({"result": "success", "user": session['username']}, ensure_ascii=False))
        return redirect(url_for('login_test'))
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
app.debug = True    # remover isso para rodar em produção!
USE_JWT = False

if __name__ == '__main__':
    engine = create_engine("mysql://root:vertrigo@"+SERVER_ADDR+"/mkradius")
    Session = sessionmaker(bind=engine)
    db_session = Session()
    app.run(host='192.168.1.14', port=5000)

# TODO: Trocar a key dos cookies e JWT_KEY para cada instância em produção
# TODO: Remover rota login_test para o release
