./env/Scripts/Activate.ps1
Start-Process python -ArgumentList .\airplane-distance-detector\src\main.py, "-O" -RedirectStandardOutput '.\console.out' -RedirectStandardError '.\console.err' -NoNewWindo
Start-Process python -ArgumentList .\src\main.py, "-O" -RedirectStandardOutput '.\console1.out' -RedirectStandardError '.\console1.err' -NoNewWindo
