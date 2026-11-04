"""Run Signal locally for development. Public hosting uses Gunicorn and site_app."""
import os
from socketserver import ThreadingMixIn
from wsgiref.simple_server import WSGIServer, make_server

from site_app import application


class LocalServer(ThreadingMixIn, WSGIServer):
    daemon_threads = True


if __name__ == '__main__':
    port = int(os.environ.get('PORT', '8765'))
    with make_server('127.0.0.1', port, application, server_class=LocalServer) as server:
        print(f'Signal OSINT: http://127.0.0.1:{port}', flush=True)
        try:
            from auth_store import AuthUnavailable, require_setup
            require_setup()
        except AuthUnavailable as exc:
            print(f'Accounts are currently unavailable: {exc} Run "python setup_admin.py" '
                  'to create the first administrator. The public workspaces still work.', flush=True)
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            print('\nServer stopped.')
