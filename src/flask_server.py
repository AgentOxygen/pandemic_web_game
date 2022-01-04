import json
from flask import Flask, render_template, request, send_file, url_for
from uuid import uuid4
from datetime import datetime

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = "../assets/"

logins = {"cam":{"display_name": "Cameron", "game_instance": "none", "logins": 0}}
instances = {}
max_players = 4

roles = {
    1:"Medic",
    2:"Scientist",
    3:"Quarantine Specialist",
    4:"Logistics Operator",
    5:"Researcher"
}

cities = {
    1:"Seattle",
    2:"San Francisco",
    3:"Los Angeles",
    4:"Helena",
    5:"Salt Lake City",
    6:"Phoenix",
    7:"Denver",
    8:"Minneapolis",
    9:"Lubbock",
    10:"San Antonio",
    11:"Chicago",
    12:"St. Louis",
    13:"New Orleans",
    14:"New York",
    15:"Richmond",
    16:"Atlanta",
    17:"Miami"
}

connections = {
    1:[2, 5, 4],
    2:[1, 5, 3],
    3:[2, 6],
    4:[1, 5, 7, 8],
    5:[1, 2, 3, 4, 6],
    6:[3, 5, 9, 10],
    7:[4, 5, 8, 9, 11, 12],
    8:[4, 7, 11, 14],
    9:[7, 6, 11],
    10:[6, 9, 12, 13],
    11:[8, 7, 12, 14],
    12:[11, 7, 14, 15, 16],
    13:[10, 16, 17],
    14:[8, 11, 12, 15],
    15:[14, 12, 16, 17],
    16:[12, 13, 15],
    17:[13, 15],
}

# For reference
init_game_data = {
    # Everyone starts in Atlanta
    "player_role_locations": {
        #"Player ID": [City number, role number]
        "A": [16, 1],
        "B": [16, 2],
        "C": [16, 4],
        "D": [16, 5] # these are examples, they're replaced in initialization
    },
    "city_disease_counts":{
        #"City number": [Virus 1, Virus 2, Virus 3, Virus 4]
        1:[0, 0, 0, 0],
        2:[0, 0, 0, 0],
        3:[0, 0, 0, 0],
        4:[0, 0, 0, 0],
        5:[0, 0, 0, 0],
        6:[0, 0, 0, 0],
        7:[0, 0, 0, 0],
        8:[0, 0, 0, 0],
        9:[0, 0, 0, 0],
        10:[0, 0, 0, 0],
        11:[0, 0, 0, 0],
        12:[0, 0, 0, 0],
        13:[0, 0, 0, 0],
        14:[0, 0, 0, 0],
        15:[0, 0, 0, 0],
        16:[0, 0, 0, 0],
        17:[0, 0, 0, 0]
    },
    "city_populations":{ # I might use these later, for now every city has 1 million people in it
        1:1000000,
        2:1000000,
        3:1000000,
        4:1000000,
        5:1000000,
        6:1000000,
        7:1000000,
        8:1000000,
        9:1000000,
        10:1000000,
        11:1000000,
        12:1000000,
        13:1000000,
        14:1000000,
        15:1000000,
        16:1000000,
        17:1000000
    },
    # List of cards drawn, might be used later
    "cards_drawn":[]
}

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


@app.route('/startgame')
def start_game():
    instance_id = request.args.get('code', default='', type=str)
    user_id = request.args.get('id', default='', type=str)
    if instance_id not in instances:
        return "invalid instance ID"
    if instances[instance_id]["host"] == user_id:
        instances[instance_id]["game_stage"] = "in_game"
        instances[instance_id]["game_data"] = init_game_data
        return "starting"
    else:
        return "not host"


@app.route('/leavegame')
def leave_game():
    instance_id = request.args.get('code', default='', type=str)
    user_id = request.args.get('id', default='', type=str)
    if instance_id in instances:
        for index, (player_id, player_dn) in enumerate(instances[instance_id]["players"]):
            if player_id == user_id:
                instances[instance_id]["players"].pop(index)
                return "left game"
        return "not in specified instance"
    else:
        return "invalid instance ID"

@app.route('/creategame')
def create_instance():
    user_id = request.args.get('id', default='', type=str)
    instance_id = str(uuid4())[:8]
    while instance_id in instances:
        instance_id = str(uuid4())[:8]
    instances[instance_id] = {"players":[], "game_data":{}, "game_stage":"init", "host":user_id}
    return instance_id


@app.route('/joingame')
def join_instance():
    instance_id = request.args.get('code', default='', type=str)
    user_id = request.args.get('id', default='', type=str)
    if instance_id in instances and user_id in logins:
        if instances[instance_id]["game_stage"] != "init":
            return "game in progress"
        for player_id, player_dn in instances[instance_id]["players"]:
            if player_id == user_id:
                return "joined"
        if len(instances[instance_id]["players"]) == max_players:
            return "max players"
        instances[instance_id]["players"].append([user_id, logins[user_id]["display_name"]])
        return instance_id
    else:
        return "failed"


@app.route("/getgame")
def get_instance():
    instance_id = request.args.get('code', default='', type=str)
    if instance_id in instances:
        instance = instances[instance_id]
        instance["ts"] = str(datetime.now())
        return json.dumps(instance)
    else:
        return "failed"


def decode_move(move, instance_id):
    # Move code will look like this:
    # [Destination 1][Dest. 2][Dest. 3][Dest. 4][(optional) cards played]
    # For each destionation code where # indicates the city number:
    # M# - move to adjacent city
    # B# - burns card to city
    # P# - moves to player in another city
    # For card played where # indicates the card number: C#
    pass
    
@app.route("/play")
def play_move():
    instance_id = request.args.get('code', default='', type=str)
    user_id = request.args.get('id', default='', type=str)
    move_code = request.args.get('move', default='', type=str)
    if instance_id in instances:
        if user_id == instances[instance_id]["game_data"]["active_player"]:
            if decode_move(instance_id, move):
                return "moved"
            else:
                return "invalid move"
        else:
            return "not active player"
    else:
        return "invalid instance ID"

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