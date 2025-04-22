Testing MCP Server

```
sudo yum install python3.12.x86_64
git clone https://github.com/manumaan/flask-mcp-weather.git
/usr/bin/python3.12 -m venv flask-mcp-weather
source ./flask-mcp-weather/bin/activate 
cd flask-mcp-weather
pip install -r requirements.txt

Run as dev: python app.py 

Run as production: gunicorn -w 4 -b 0.0.0.0:5000 app:app
```
