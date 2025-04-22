Testing MCP Server
Test push
```
version: 1
frontend:
  phases:
    preBuild:
      commands:
        - pip install -r requirements.txt
    build:
      commands:
        - gunicorn -w 4 -b 0.0.0.0:5000 app:app
  artifacts:
    baseDirectory: /
    files:
      - '**/*'
  cache:
    paths:
      - '**/*'
```
