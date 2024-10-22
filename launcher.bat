call .venv\Scripts\activate %*
python.exe -m pip install --upgrade pip %*
python prompt_handler_SporkV2.py %*
deactivate
pause