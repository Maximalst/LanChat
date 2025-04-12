from flask import Flask, request, redirect, send_from_directory, make_response
from markupsafe import Markup
from datetime import datetime
import os
import json

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

LOG_FILE = 'chat_log.json'
messages = []

# Vorhandene Nachrichten laden
if os.path.exists(LOG_FILE):
    with open(LOG_FILE, 'r', encoding='utf-8') as f:
        messages = json.load(f)

def save_messages():
    with open(LOG_FILE, 'w', encoding='utf-8') as f:
        json.dump(messages, f, ensure_ascii=False, indent=2)

@app.route('/', methods=['GET'])
def chat():
    username = request.cookies.get('username')

    if not username:
        return '''
<!DOCTYPE html>
<html lang="de" data-bs-theme="dark">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>LAN of Maxi – Name setzen</title>
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
</head>
<body class="bg-black text-light">
  <div class="container mt-5">
    <div class="bg-dark text-light p-5 rounded shadow">
      <h1 class="text-center mb-4">Willkommen im LAN Chat 🎮</h1>
      <p class="text-center">Bitte gib deinen Namen ein, um dem Chat beizutreten:</p>
      <form method="POST" action="/setname" class="mx-auto" style="max-width: 400px;">
        <div class="mb-3">
          <input type="text" name="user" class="form-control form-control-lg" placeholder="Dein Name" required>
        </div>
        <button type="submit" class="btn btn-success btn-lg w-100">Beitreten</button>
      </form>
    </div>
  </div>
</body>
</html>
        '''

    return f'''
<!DOCTYPE html>
<html lang="de" data-bs-theme="dark">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Lan Chat – Chat</title>
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
  <script>
    function loadMessages() {{
        fetch('/messages')
            .then(response => response.text())
            .then(html => {{
                document.getElementById('messages').innerHTML = html;
                var msgBox = document.getElementById('messages');
                msgBox.scrollTop = 0;
            }});
    }}

    function sendMessage(e) {{
        e.preventDefault();
        const form = document.getElementById('chatForm');
        const formData = new FormData(form);
        fetch('/send', {{
            method: 'POST',
            body: formData
        }}).then(() => {{
            form.reset();
            loadMessages();
        }});
    }}

    setInterval(loadMessages, 3000);
    window.onload = loadMessages;
  </script>
</head>
<body class="bg-black text-light">
  <div class="container mt-5">
    <div class="bg-dark text-light p-5 rounded shadow">
      <h1 class="text-center mb-4">LAN of Maxi 🎮</h1>
      <p class="text-center text-secondary">Angemeldet als: <strong>{username}</strong></p>

      <form id="chatForm" onsubmit="sendMessage(event)" enctype="multipart/form-data" class="mb-4">
        <input type="hidden" name="user" value="{username}">
        <div class="mb-3">
          <input type="text" name="message" class="form-control form-control-lg" placeholder="Deine Nachricht">
        </div>
        <div class="mb-3">
          <input type="file" name="file" class="form-control">
        </div>
        <button type="submit" class="btn btn-primary btn-lg w-100">Senden / Hochladen</button>
      </form>

      <div id="messages" class="card p-3 bg-dark text-white border-light" style="max-height: 60vh; overflow-y: auto;"></div>
    </div>
  </div>
</body>
</html>
    '''

@app.route('/setname', methods=['POST'])
def setname():
    username = request.form.get('user', 'Anonym')
    response = make_response(redirect('/'))
    response.set_cookie('username', username)
    return response

@app.route('/send', methods=['POST'])
def send():
    user = request.form.get('user', 'Anonym')
    message = request.form.get('message', '').strip()
    file = request.files.get('file')
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    ip = request.remote_addr

    if message:
        if len(message) > 1000:
            message = message[:1000] + '...'
        print(f"[{timestamp}] [IP: {ip}] {user} schrieb: {message}")
        messages.append({'user': user, 'text': message, 'time': timestamp, 'ip': ip})
        save_messages()

    if file and file.filename:
        safe_filename = f"{timestamp.replace(':', '-')}_{file.filename}"
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], safe_filename)
        file.save(filepath)
        file_link = f"<a href='/uploads/{safe_filename}' download>{file.filename}</a>"
        print(f"[{timestamp}] [IP: {ip}] {user} lud Datei hoch: {file.filename}")
        messages.append({'user': user, 'text': file_link, 'time': timestamp, 'ip': ip})
        save_messages()

    return ('', 204)

@app.route('/messages')
def message_list():
    html = ''
    for msg in reversed(messages):
        html += f'''
        <div class="mb-2">
          <strong>{msg['user']}</strong>
          <small class="text-muted">({msg['time']} | IP: {msg.get('ip', 'unbekannt')})</small><br>
          {Markup(msg['text'])}
        </div>
        <hr>
        '''
    return html

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    print("Server läuft auf http://0.0.0.0:5000")
    app.run(host='0.0.0.0', port=5000)
