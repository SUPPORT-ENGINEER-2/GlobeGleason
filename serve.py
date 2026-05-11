#!/usr/bin/env python3
"""Standalone live server runner for GlobeGleaason."""

from http.server import HTTPServer, SimpleHTTPRequestHandler
import argparse
import os
import signal
import sys
import webbrowser


def main():
    parser = argparse.ArgumentParser(
        description='Run a simple local web server for GlobeGleaason.'
    )
    parser.add_argument(
        '--host',
        default='127.0.0.1',
        help='Hostname to serve on (default: 127.0.0.1)'
    )
    parser.add_argument(
        '--port',
        type=int,
        default=8000,
        help='Port to serve on (default: 8000)'
    )
    parser.add_argument(
        '--root',
        default=os.getcwd(),
        help='Folder to serve (default: current working directory)'
    )
    parser.add_argument(
        '--no-browser',
        action='store_true',
        help='Do not open the browser automatically'
    )
    args = parser.parse_args()

    project_root = os.path.abspath(args.root)
    if not os.path.isdir(project_root):
        raise FileNotFoundError(f'Specified root folder does not exist: {project_root}')
    os.chdir(project_root)

    url = f'http://{args.host}:{args.port}/index.html'
    print(f'Serving GlobeGleaason from: {project_root}')
    print(f'Open this URL in your browser: {url}')

    if not args.no_browser:
        try:
            webbrowser.open(url)
        except Exception:
            pass

    server = HTTPServer((args.host, args.port), SimpleHTTPRequestHandler)

    def stop_server(signum, frame):
        print('\nSignal received, shutting down server...')
        raise KeyboardInterrupt

    signal.signal(signal.SIGINT, stop_server)
    if hasattr(signal, 'SIGTERM'):
        signal.signal(signal.SIGTERM, stop_server)

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print('\nKeyboard interrupt received, shutting down server...')
    finally:
        server.server_close()
        print('Server stopped.')


if __name__ == '__main__':
    main()
