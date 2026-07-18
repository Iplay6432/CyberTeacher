from werkzeug.middleware.dispatcher import DispatcherMiddleware
from werkzeug.serving import run_simple
from project import create_app
from project.challenge_websites.challTemplate import challTemplate as chall_template_app
import os

URL = os.environ.get('URL', 'localhost')
PORT = int(os.environ.get('PORT', 5000))
DEBUG = os.environ.get("FLASK_DEBUG", "0")

main_app = create_app()

application = DispatcherMiddleware(main_app, {
    "/chall0": chall_template_app,
})


if __name__ == "__main__":
    run_simple(URL, PORT, application, use_debugger=DEBUG)
