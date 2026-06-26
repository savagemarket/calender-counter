from datetime import datetime, timedelta, timezone
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from json import dumps
from random import randint
from urllib.parse import parse_qs, urlparse


class CalendarCounterHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        parsed = urlparse(self.path)
        if parsed.path == "/api/random-date":
            self.send_random_date(parsed.query)
            return
        super().do_GET()

    def send_random_date(self, query):
        values = parse_qs(query)
        minimum = self.safe_int(values.get("min", ["1"])[0], 1)
        maximum = self.safe_int(values.get("max", ["365"])[0], 365)
        mode = values.get("mode", ["balanced"])[0]
        low = max(1, min(minimum, maximum))
        high = max(low, maximum)
        days = randint(low, high)

        target = datetime.now(timezone.utc) + timedelta(days=days)
        target, note = self.apply_mode(target, mode, days)

        payload = {
            "iso": target.isoformat().replace("+00:00", "Z"),
            "days": days,
            "mode": mode,
            "note": note,
            "server": "Python http.server with custom JSON endpoint",
        }

        body = dumps(payload, indent=2).encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def safe_int(self, value, fallback):
        try:
            return int(value)
        except (TypeError, ValueError):
            return fallback

    def apply_mode(self, target, mode, days):
        if mode == "weekend":
            while target.weekday() not in (5, 6):
                target += timedelta(days=1)
            target = target.replace(hour=10, minute=randint(0, 59), second=0, microsecond=0)
            return target, f"Python selected a weekend target after starting from {days} random days."

        if mode == "quarter":
            quarter_end_month = ((target.month - 1) // 3 + 1) * 3
            next_month = quarter_end_month + 1
            year = target.year
            if next_month == 13:
                next_month = 1
                year += 1
            first_next_month = datetime(year, next_month, 1, tzinfo=timezone.utc)
            target = first_next_month - timedelta(days=1)
            target = target.replace(hour=17, minute=0, second=0, microsecond=0)
            return target, f"Python snapped the random date toward the nearest quarter end."

        if mode == "chaos":
            target = target.replace(
                hour=randint(0, 23),
                minute=randint(0, 59),
                second=randint(0, 59),
                microsecond=randint(0, 999999),
            )
            return target, f"Python generated a chaos-clock moment {days} days from now."

        target = target.replace(hour=randint(8, 20), minute=randint(0, 59), second=randint(0, 59), microsecond=0)
        return target, f"Python generated a balanced target {days} days from now."


def main():
    host = "127.0.0.1"
    port = 8000
    server = ThreadingHTTPServer((host, port), CalendarCounterHandler)
    print(f"Calendar Counter Lab is running at http://{host}:{port}/index.html")
    print(f"Random date API is available at http://{host}:{port}/api/random-date?min=7&max=365&mode=balanced")
    server.serve_forever()


if __name__ == "__main__":
    main()
