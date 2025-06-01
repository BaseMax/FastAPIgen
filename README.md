# FastAPIgen (Py API Generator)

**Py API Generator** is a Python-based code generation tool that lets you rapidly scaffold a fully functional FastAPI backend using a simple JSON configuration file.

It supports:
- FastAPI routing with CRUD operations
- SQLAlchemy models
- Pydantic schemas
- Optional API key-based authentication
- SQLite, PostgreSQL, or MySQL databases

## Features

- 🧱 Scaffold FastAPI apps in seconds
- 🗂️ Auto-generate routers, models, schemas, and database configs
- 🔐 Optional authentication using API keys
- 🧪 Lightweight and customizable template system using Jinja2

## Usage

1. Create a JSON config file with routes and models.
2. Run the generator:

```bash
python generator.py config.json
```

3. Your FastAPI project will be generated in a new folder named after your project.

## Example

Example `config.json` file:

```json
{
  "project_name": "todo_api",
  "auth": true,
  "database": {
    "type": "sqlite",
    "url": "sqlite:///todo.db"
  },
  "models": [
    {
      "name": "Todo",
      "fields": {
        "id": "integer",
        "title": "string",
        "completed": "boolean"
      }
    }
  ],
  "routes": [
    { "path": "/todos", "methods": ["GET", "POST"], "resource": "todo" },
    { "path": "/todos/{id}", "methods": ["GET", "PUT", "DELETE"], "resource": "todo" }
  ]
}
```

## Summary

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

## License

MIT License  
© 2025 Max Base

---

Generated with ❤️ by [BaseMax](https://github.com/BaseMax)
