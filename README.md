# OnionAtlas

A field guide to the onion grid: a static directory of Tor hidden
services, served as a Tor hidden service itself.

## Layout

```
public/index.html   The directory page (8 entries)
serve.py            Static file server for the local port
tor-keys/           Hidden service keys (NEVER committed, gitignored)
```

## Run

```bash
python3 serve.py
```

The service listens on the local port mapped by the Tor hidden service
config (`HiddenServicePort 80 127.0.0.1:18097`).

## Note

`tor-keys/` holds the private key that owns the `.onion` address. It is
excluded from version control on purpose: anyone with that key can
impersonate the address. Never commit it, never share it.
