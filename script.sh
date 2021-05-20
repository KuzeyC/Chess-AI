if [ ! -f /ce301_cimen_kuzey ]; then
    python3 -m venv ce301_cimen_kuzey
    source ce301_cimen_kuzey/bin/activate
    pip install -r requirements.txt
else
    source ce301_cimen_kuzey/bin/activate
    clear
    start.py
fi