IF NOT EXIST ce301_cimen_kuzey (
    py -m venv ce301_cimen_kuzey
    call ce301_cimen_kuzey\Scripts\activate
    pip install -r requirements.txt
) ELSE (
    call ce301_cimen_kuzey\Scripts\activate
    cls
    call start.py
)
