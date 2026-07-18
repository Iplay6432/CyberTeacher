import os
import flask
from pathlib import Path
import json

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FLAG = "flag{dummy_flag}"
CHALL_NUM = 0


if Path(BASE_DIR).joinpath("hosted").is_file():
    challTemplate = flask.Flask(__name__, template_folder=Path(BASE_DIR).joinpath("chall_templates"), static_folder=Path(BASE_DIR).joinpath("chall_statics"))
    flag_location = Path(BASE_DIR).parent.joinpath("data").joinpath("flags.json")
    with open(flag_location, "r") as f:
        flags = json.load(f)
        FLAG = flags["flags"][CHALL_NUM]["flag"]
else:
    challTemplate = flask.Flask(__name__)
    
@challTemplate.route("/")
def index():
    return FLAG


if __name__ == "__main__" and not Path(BASE_DIR).joinpath("hosted").is_file():
    challTemplate.run(host="0.0.0.0", port=5000)