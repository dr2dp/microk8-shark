from flask import Flask, jsonify
import socket
import os

app = Flask(__name__)

@app.route('/')
def home():
    return jsonify({
        'message': 'Hello from MicroK8s!',
        'hostname': socket.gethostname(),
        'pod_ip': os.environ.get('POD_IP', 'unknown')
    })

@app.route('/health')
def health():
    return jsonify({'status': 'healthy'}), 200

@app.route('/ready')
def ready():
    return jsonify({'status': 'ready'}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)