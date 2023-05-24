import flask
import socket
import os

app = flask.Flask(__name__)
app.config["DEBUG"] = True


@app.route('/', methods=['POST','DELETE'])
def port():
    if flask.request.method == 'POST':
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.bind(('', 0))
            sPort = s.getsockname()[1]
            s.close()

            dIp = flask.request.form['dIp']
            dPort = flask.request.form['dPort']

            os.system('redir 0.0.0.0:{} {}:{}'.format(sPort, dIp, dPort))

            return {"status": "SUCCESS", "port": sPort}
        except Exception as e:
            print(e)
            return {"status": "FAILURE"}

    elif flask.request.method == 'DELETE':
        try:
            sPort = flask.request.form['sPort']
            os.system('pkill -f "redir 0.0.0.0 {}"'.format(sPort))
            return {"status": "SUCCESS"}
        except Exception as e:
            print(e)
            return {"status": "FAILURE"}

app.run(host='0.0.0.0', port=8080)