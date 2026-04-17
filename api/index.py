from vercel_runtime import Request, Response
import sys
sys.path.insert(0, '/var/task')

from app import app as flask_app

def handler(request: Request):
    return flask_app(request)
