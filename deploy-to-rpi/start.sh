cd /home/pi/lights-widget/deploy-to-rpi
. venv/bin/activate
PYTHONPATH=".:build/lib.linux-armv7l-2.7" flask run --host=0.0.0.0 --port=8080
