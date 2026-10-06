# Fieldwork — local jersey portfolio

Start the website from this directory:

```sh
python3 server.py
```

Open http://127.0.0.1:4173. Keep the server running while using the website. Stop it with Ctrl+C.

If that port is already in use, choose another one:

```sh
PORT=4174 python3 server.py
```

Then open http://127.0.0.1:4174.

The collection is saved in `collection.json` next to `server.py` after the first change. Photos are resized and included in this file. Back up this file to preserve your collection. The website's Export collection button also downloads a copy.

Six fictional examples and illustrative jersey photos are provided. Use Clear examples to remove them, and Add a jersey to enter your real collection. Search matches names, teams, players, numbers, years, notes, condition, color and size. Filters support sport, multiple colors, age and size; sort by recently added, oldest, newest, or name. Open a card to view, edit, or remove it.

The server listens only on this computer. It uses Python's standard library and requires no package installation. This is a personal local site, not a public hosting server.

## Saved collection

`collection.json` is the file-backed database, including photo data for any uploaded jerseys. This repository includes a snapshot of the local collection. Local changes do not automatically sync to GitHub; commit and push the updated file when you want to refresh that snapshot.
