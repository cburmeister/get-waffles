get-waffles
===

Fetch freeleech torrents from waffles.fm with at least one leecher for
automatic ratio gains.


## Required

1. An account on [waffles.fm](https://waffles.fm/). Don't ask me for an invite.
2. An operational [Transmission daemon](https://www.transmissionbt.com/) with
   RPC enabled.

## Setup

Install the required python packages:
```bash
$ pip install -r requirements.txt
```

Export a few required environment variables:
```bash
export WAFFLES_USER='username'
export WAFFLES_PASS='password'
export TRANSMISSION_HOST='10.0.0.12'
export TRANSMISSION_PORT=9091
```

Get them waffles:
```bash
python get-waffles.py
```
