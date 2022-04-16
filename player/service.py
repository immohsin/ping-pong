import atexit
import logging

from flask import Flask

from player.server import PlayerSever
from player.config import PlayerConfig

# Flask app
app = Flask(__name__)

# Logger Config
logging.basicConfig(
    filename="player/players.log", format="%(asctime)s %(message)s", filemode="a"
)
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Player Server setup
config = PlayerConfig.read_config()
server = PlayerSever(config, logger)
# Handle graceful shutdown
atexit.register(server.stop)
port = config.get_port()
server.start()
