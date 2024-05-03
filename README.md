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
STREAM_URL=<url for RTSP stream>
IMAGE_ENDPOINT=<url to fetch image>
```

Run polling script

```
python periodically_test.py
```

Run streaming script

```
python rtsp_stream_test.py
```