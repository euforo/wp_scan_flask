from flask import render_template
import os
from flask import Flask
import paramiko


app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/contact')
def contact():
    return render_template('contact.html')


@app.route('/doom')
def doom():
    return render_template('doom_crazy.html')

@app.route('/comandin')
def run_command():
    domain = request.form.get('domain', methods=['POST'])
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    host = 'capricornio.internet-magician.xyz'
    username = 'hatter'
    password = 'Locaweb@102030'
    #private_key_path = os.path.expanduser('~/home/flask/pk')
    private_key_path = '/root/flask/pk.key'  # Caminho para a chave privada
    command ='wpscan --url http://{domain}' 
    
    try:
        private_key = paramiko.RSAKey.from_private_key_file(private_key_path)
        ssh.connect(host, username=username, pkey=private_key)
        stdin, stdout, stderr = ssh.exec_command(command)
        result = stdout.read().decode('utf-8')
        return render_template('scan.html', result=result)
    except paramiko.AuthenticationException as err:
        return f'Falha na autenticação SSH: {str(err)}'
    except paramiko.SSHException as e:
        return f'Erro na conexão SSH: {str(e)}'
    finally:
        ssh.close()



if __name__ == '__main__':
    app.run()
