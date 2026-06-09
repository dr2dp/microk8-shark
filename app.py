from flask import Flask
import socket
import os

app = Flask(__name__)

@app.route('/')
def home():
    hostname = socket.gethostname()
    pod_ip = os.environ.get('POD_IP', 'unknown')

    ascii_art = f"""                                                            

          ":"
        ___:____     |"\/"|
      ,'        `.    \  /
      |  O        \___/  |
    ~^~^~^~^~^~^~^~^~^~^~^~^~

  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  Pod Hostname:  {hostname}
  Pod IP:        {pod_ip}
  Status:        Running

  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

    """
    return ascii_art, 200, {'Content-Type': 'text/plain; charset=utf-8'}

@app.route('/health')
def health():
    return 'OK', 200

@app.route('/ready')
def ready():
    return 'OK', 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
