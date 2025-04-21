cd .\my-website-tiktok-server\
python -m venv venv
.\venv\Scripts\activate
source ./venv/bin/activate
pip install -r requirements.txt
pip freeze > requirements.txt
fastapi dev main.py --port 8000
uvicorn main:app --port 8000 --reload
cd my-website-tiktok-server/ && source venv/bin/activate && fastapi dev main.py
