#!/bin/bash
set -e

apt-get update
apt-get install --yes python3 python3-distutils wget git ffmpeg

python3 -c "import urllib.request; open('get-pip.py','wb').write(urllib.request.urlopen('https://bootstrap.pypa.io/get-pip.py').read())"
python3 get-pip.py

cd /root
git clone https://github.com/blairexico/whisper-api.git
cd whisper-api/app

pip install --requirement requirements.txt

uvicorn main:app --host 0.0.0.0 --port 7860
