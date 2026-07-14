from werkzeug.middleware.dispatcher import DispatcherMiddleware
from werkzeug.serving import run_simple

from project import create_app
from project.challenge_websites.challTemplate import challTemplate as chall_template_app

main_app = create_app()

application = DispatcherMiddleware(main_app, {
    "/chall0": chall_template_app,
})


if __name__ == "__main__":
    run_simple("0.0.0.0", 5000, application)