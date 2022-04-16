import atexit
import logging

from flask import Flask, request

from referee.server import RefereeSever
from referee.config import RefereeConfig

# Flask app
app = Flask(__name__)

# logging config
logging.basicConfig(
    filename="referee/referee.log", format="%(asctime)s %(message)s", filemode="a"
)

logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Ping Pong server setup
config = RefereeConfig.read_config()
server = RefereeSever(config, logger)
server.start()

# Handle graceful shutdown
atexit.register(server.stop)


@app.route("/notify-attack")
def notify_attack():
    try:
        args = request.args
        guessed_number = args.get("guessed_number")
        opponent = args.get("opponent")
        game_id = args.get("game-id")
        server.process_attack_request(guessed_number, opponent, game_id)
        return "Success", 200
    except KeyError as e:
        return str(e), 500
    except ValueError as e:
        return str(e), 500


@app.route("/join-championship")
def championship_status():
    try:
        args = request.args
        name = args.get("name")
        server.notify_player_joining(name)
        return "Success", 200
    except KeyError as e:
        return str(e), 500
    except ValueError as e:
        return str(e), 500


@app.route("/start-championship")
def start_championship():
    try:
        server.start_championship()
        return "Success", 200
    except KeyError as e:
        return str(e), 500
    except ValueError as e:
        return str(e), 500


@app.route("/notify-status")
def notify_status():
    try:
        args = request.args
        defended = args.get("defended")
        game_id = args.get("game-id")
        server.process_defence_request(game_id, defended)
    except ValueError as e:
        return str(e), 500
    except KeyError as e:
        return str(e), 500
    return "Success", 200
