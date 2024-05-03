# heron tracker

Set up venv
```
python3 -m venv venv
source venv/bin/activate
```

Install requirements

```
pip install -r requirements.txt
```

Set up .env

```
ENDPOINT=<endpoint to call with image data>
IMAGE_ENDPOINT=<url to fetch image>
```

Run script

```
python periodically_test.py
```