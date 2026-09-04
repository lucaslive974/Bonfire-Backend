from waitress import serve

from app import BonfireApp
from core.cli import BonfireArgumentParser
from utils.logger import logger

if __name__ == "__main__":
    args = BonfireArgumentParser()
    app = BonfireApp(__name__)

    logger.info(f"::Application listening on port {args.port()}::")
    if args.isDebug():
        logger.warn("::Application running in debug mode::")
        app.run(debug=True, port=args.port())
    else:
        logger.warn("::Application running in production mode by WSGI::")
        serve(app, host="0.0.0.0", port=args.port())
