python -m venv .venv %*
.\.venv\Scripts\activate %*
.\.venv\Scripts\python.exe -m pip install --upgrade pip %*
.\.venv\Scripts\python.exe pip install -r .\requirements.txt %*
pause