import json
from flask import Flask, render_template, request, send_file

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = "../assets/"

logins = {}

@app.route('/')
def main():
    return render_template("main.html")

@app.route('/createlogin')
def create_login():
    login_id = request.args.get('id', default='', type=str)
    login_dn = request.args.get('dn', default='', type=str)
    logins[login_id] = {"display_name": login_dn, "game_instance": "none", "logins": 0}
    return json.dumps(logins[login_id])

@app.route('/login')
def login():
    login_id = request.args.get('id', default='', type=str)
    if login_id in logins:
        logins[login_id]["logins"] += 1
        return json.dumps(logins[login_id])
    else:
        return "no_login"

##### Chat Feature to Demonstrate Multiplayer
chat = []
@app.route('/chat')
def get_chat():
    chat_str = ""
    for msg in chat:
        chat_str += f"<br>{msg}"
    return chat_str
    
@app.route('/sendchat')
def send_chat():
    msg = request.args.get('msg', default='', type=str)
    chat.append(msg)
    return msg
#####
    
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)