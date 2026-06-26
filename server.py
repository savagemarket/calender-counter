from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer


def main():
    host = "127.0.0.1"
    port = 8000
    server = ThreadingHTTPServer((host, port), SimpleHTTPRequestHandler)
    print(f"Calendar Counter is running at http://{host}:{port}/index.html")
    server.serve_forever()


if __name__ == "__main__":
    main()
