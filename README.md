# py-api-generator

## Python API Project Generator

Reads a JSON config file and generates a FastAPI-based project with features such as:

- Route generation
- Input validation
- JSON responses
- Redirects
- Headers
- Query parameters
- Path parameters
- Response status codes
- Middleware (CORS)

## Using

```bash
$ python generator.py config.json

$ pip install -r requirements.txt

$ uvicorn main:app --reload
INFO:     Will watch for changes in these directories: ['C:\\Users\\MAX\\py-api-generator\\my_api']
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [14544] using StatReload
INFO:     Started server process [13976]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

Copyright 2025, Max Base
