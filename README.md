# Calendar Counter Lab

Calendar Counter Lab is a small experimental countdown app that mixes plain HTML, CSS, browser JavaScript, and a tiny Python server. It generates a random future moment, calculates how much time remains from now, and updates the countdown every second.

The project started as a simple calendar counter, but it now includes multiple generation modes, a Python JSON endpoint, browser fallback logic, local saved history, and extra calendar-difference calculations.

## Features

- Random future date generation from a user-defined day range.
- Real-time countdown for days, hours, minutes, and seconds.
- Multiple generation modes:
  - Balanced random
  - Weekend-focused dates
  - Quarter-end style dates
  - Chaos clock with fully randomized time
- Python-powered JSON API at `/api/random-date`.
- Browser JavaScript fallback if the API is unavailable.
- Local history saved with `localStorage`.
- Reload saved countdown targets from browser history.
- Responsive layout for desktop and mobile screens.
- No external dependencies, build tools, package managers, or frameworks.

## Tech Stack

This repository intentionally mixes a few simple technologies in one place:

- `index.html` contains the user interface, CSS styling, and browser-side JavaScript.
- `server.py` serves the HTML file and provides a custom JSON endpoint.
- `README.md` documents how the project works and how to run it.

The app works as a static file, but the full experience is best through the Python server because the server can generate random dates through the API.

## Quick Start

Run the Python server:

```powershell
python server.py
```

Open the app in your browser:

```text
http://127.0.0.1:8000/index.html
```

You can also open `index.html` directly in a browser. In that mode, the Python API will not be available, so the JavaScript fallback generator will be used automatically.

## API Example

The Python server exposes a small endpoint:

```text
/api/random-date?min=7&max=365&mode=balanced
```

Example response:

```json
{
  "iso": "2027-03-14T11:24:08Z",
  "days": 261,
  "mode": "balanced",
  "note": "Python generated a balanced target 261 days from now.",
  "server": "Python http.server with custom JSON endpoint"
}
```

Supported `mode` values:

- `balanced`
- `weekend`
- `quarter`
- `chaos`

## How It Works

1. The browser reads the minimum and maximum day range from the form.
2. JavaScript asks the Python API for a random future date.
3. If the API responds, the countdown uses the server-generated date.
4. If the API is unavailable, JavaScript generates the date in the browser.
5. The countdown updates every second using the current local time.
6. Saved runs are stored in browser `localStorage` and can be loaded later.

## File Overview

```text
.
├── index.html   # HTML, CSS, and JavaScript app
├── server.py    # Python static server plus random-date API
└── README.md    # Project documentation
```

## Notes

The repository name keeps the original spelling: `calender-counter`. The app title uses the standard spelling, `Calendar Counter Lab`.

This is designed as a compact learning project rather than a production app. It is useful for experimenting with date math, countdown timers, browser storage, API calls, and simple Python HTTP handlers.
