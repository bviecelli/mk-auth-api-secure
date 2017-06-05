from flask import Flask, session, redirect, url_for, escape, request
import requests, json

app = Flask(__name__)


def mkLogin(username, passwd):
    resp = requests.get('http://192.168.1.200/api/83fdf5e05ffb52a01f37c22b27e0da07/cliente/list/'+username)
    if resp.status_code == 200:
        json = resp.json()
        if json == 'NULL':
            return False
        if json['dados'][0]['senha'] == passwd:
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
    req = requests.get('http://192.168.1.200/api/83fdf5e05ffb52a01f37c22b27e0da07/titulo/list')
    if req.status_code != 200:
        return 'Error: mk-auth internal server error!'
    resp = req.json()
    if resp == 'NULL':
        return 'Error: content not found!'
    billList = []
    for item in resp['titulos']:
        if item['login'] == session['username']:
            billList.append(item)
    json_ret = json.dumps(billList)
    return json_ret


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if mkLogin(request.form['username'], request.form['password']):
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
    app.run()

# TODO: Ajustar os retornos das páginas para formato JSON
# TODO: Trocar a key dos cookies
# TODO: Trocar login via form para JSON
# TODO: Utilizar JWT para todo o conteúdo JSON
