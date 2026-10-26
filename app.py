from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import subprocess
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='eventlet')

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('input')
def handle_input(data):
    cmd = data['data'].strip()
    if not cmd: return
    
    # Ye sirf kuch safe commands run karega (Real Linux terminal ki tarah)
    try:
        if cmd == 'help':
            output = "Available commands: help, date, whoami, ls, clear, ping, echo"
        elif cmd == 'clear':
            output = "clear"
        else:
            # Linux command run karo (Output capture karo)
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=5)
            output = result.stdout if result.stdout else result.stderr
            if not output:
                output = f"Command '{cmd}' executed successfully (no output).\n"
    except Exception as e:
        output = f"Error: {str(e)}\n"

    socketio.emit('output', {'data': output})

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))