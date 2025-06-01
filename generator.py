import json
import os
from jinja2 import Environment, Template

templates = {
    'main.py.j2': '''\
from fastapi import FastAPI
{% if auth %}
from utils.auth import get_api_key
{% endif %}
{% if database %}
from database import database
{% endif %}
from routers import {{ resources|join(', ') }}

app = FastAPI()

# Include routers
{% for resource in resources %}
app.include_router({{ resource }}.router)
{% endfor %}

# Startup and shutdown events
{% if database %}
@app.on_event("startup")
async def startup():
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()
{% endif %}
''',

    'database.py.j2': '''\
from databases import Database
from sqlalchemy import create_engine, MetaData
import os

DATABASE_URL = os.environ.get("DATABASE_URL", "{{ database_url }}")

database = Database(DATABASE_URL)
metadata = MetaData()

# Import models to register them with metadata
from models import {{ models|join(', ') }}
''',

    'models.py.j2': '''\
from sqlalchemy import Table, Column, Integer, String, Float, MetaData

metadata = MetaData()

{% for model in models %}
{{ model.name }} = Table(
    "{{ model.name.lower() }}",
    metadata,
    Column("id", Integer, primary_key=True),
    {% for field, typ in model.fields.items() if field != 'id' %}
    Column("{{ field }}", {{ typ|capitalize }}),
    {% endfor %}
)
{% endfor %}
''',

    'schemas.py.j2': '''\
from pydantic import BaseModel

{% for model in models %}
class {{ model.name }}Request(BaseModel):
    {% for field, typ in model.fields.items() if field != 'id' %}
    {{ field }}: {{ typ }}
    {% endfor %}

class {{ model.name }}Response(BaseModel):
    {% for field, typ in model.fields.items() %}
    {{ field }}: {{ typ }}
    {% endfor %}
{% endfor %}
''',

    'router.py.j2': '''\
from fastapi import APIRouter, Depends, HTTPException
{% if database %}
from database import database
from models import {{ model.name }}
{% endif %}
from schemas import {{ model.name }}Request, {{ model.name }}Response
{% if auth %}
from utils.auth import get_api_key
{% endif %}

router = APIRouter()

{% for route in routes %}
{% for method in route.methods %}
{% if '{' in route.path and '}' in route.path %}
{% set param = route.path.split('{')[1].split('}')[0] %}
{% if method == 'GET' %}
@router.get("{{ route.path }}")
async def get_{{ model.name.lower() }}({{ param }}: int{% if auth %}, api_key: str = Depends(get_api_key){% endif %}):
    {% if database %}
    query = {{ model.name }}.select().where({{ model.name }}.c.id == {{ param }})
    item = await database.fetch_one(query)
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return item
    {% else %}
    # TODO: Implement GET {{ route.path }}
    return {"message": "GET {{ route.path }}"}
    {% endif %}
{% elif method == 'PUT' %}
@router.put("{{ route.path }}")
async def update_{{ model.name.lower() }}({{ param }}: int, {{ model.name.lower() }}: {{ model.name }}Request{% if auth %}, api_key: str = Depends(get_api_key){% endif %}):
    {% if database %}
    query = {{ model.name }}.select().where({{ model.name }}.c.id == {{ param }})
    item = await database.fetch_one(query)
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    update_query = {{ model.name }}.update().where({{ model.name }}.c.id == {{ param }}).values(**{{ model.name.lower() }}.dict())
    await database.execute(update_query)
    return {"message": "Updated"}
    {% else %}
    # TODO: Implement PUT {{ route.path }}
    return {"message": "PUT {{ route.path }}"}
    {% endif %}
{% elif method == 'DELETE' %}
@router.delete("{{ route.path }}")
async def delete_{{ model.name.lower() }}({{ param }}: int{% if auth %}, api_key: str = Depends(get_api_key){% endif %}):
    {% if database %}
    query = {{ model.name }}.select().where({{ model.name }}.c.id == {{ param }})
    item = await database.fetch_one(query)
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    delete_query = {{ model.name }}.delete().where({{ model.name }}.c.id == {{ param }})
    await database.execute(delete_query)
    return {"message": "Deleted"}
    {% else %}
    # TODO: Implement DELETE {{ route.path }}
    return {"message": "DELETE {{ route.path }}"}
    {% endif %}
{% endif %}
{% else %}
{% if method == 'GET' %}
@router.get("{{ route.path }}")
async def list_{{ model.name.lower() }}s({% if auth %}api_key: str = Depends(get_api_key){% endif %}):
    {% if database %}
    query = {{ model.name }}.select()
    return await database.fetch_all(query)
    {% else %}
    # TODO: Implement GET {{ route.path }}
    return {"message": "GET {{ route.path }}"}
    {% endif %}
{% elif method == 'POST' %}
@router.post("{{ route.path }}")
async def create_{{ model.name.lower() }}({{ model.name.lower() }}: {{ model.name }}Request{% if auth %}, api_key: str = Depends(get_api_key){% endif %}):
    {% if database %}
    query = {{ model.name }}.insert().values(**{{ model.name.lower() }}.dict())
    last_id = await database.execute(query)
    return {**{{ model.name.lower() }}.dict(), "id": last_id}
    {% else %}
    # TODO: Implement POST {{ route.path }}
    return {"message": "POST {{ route.path }}"}
    {% endif %}
{% endif %}
{% endif %}
{% endfor %}
{% endfor %}
''',

    'auth.py.j2': '''\
from fastapi import Header, HTTPException
import os

API_KEY = os.environ.get("API_KEY")

async def get_api_key(api_key: str = Header(...)):
    if api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API Key")
    return api_key
''',

    'requirements.txt.j2': '''\
aiosqlite
fastapi
uvicorn
pydantic
{% if database %}
databases
sqlalchemy
{% if database.type == 'postgresql' %}
asyncpg
{% elif database.type == 'mysql' %}
aiomysql
{% endif %}
{% endif %}
''',

    '.env.example.j2': '''\
API_KEY=your_api_key_here
{% if database %}
DATABASE_URL={{ database.get('url', 'sqlite:///mydb.db') }}
{% endif %}
'''
}

def generate_project(config_path, output_dir='.'):
    with open(config_path) as f:
        config = json.load(f)

    project_name = config['project_name']
    resources = set(route['resource'] for route in config['routes'])
    models = {model['name'].lower(): model for model in config.get('models', [])}

    # Validate that all resources have corresponding models
    missing_models = [resource for resource in resources if resource not in models]
    if missing_models:
        raise ValueError(f"Missing models for resources: {', '.join(missing_models)}")

    project_dir = os.path.join(output_dir, project_name)
    os.makedirs(project_dir, exist_ok=True)

    env = Environment()

    def render_template(template_name, **context):
        template = env.from_string(templates[template_name])
        return template.render(**context)

    main_content = render_template('main.py.j2',
        auth=config.get('auth'),
        database=config.get('database'),
        resources=resources,
        project_name=project_name
    )
    with open(os.path.join(project_dir, 'main.py'), 'w') as f:
        f.write(main_content)

    if config.get('database'):
        database_config = config.get('database', {})
        if isinstance(database_config, dict):
            database_url = database_config.get('url', f"sqlite:///{project_name}.db")
        else:
            database_url = f"sqlite:///{project_name}.db"
        model_names = [model['name'] for model in config.get('models', [])]
        db_content = render_template('database.py.j2',
            project_name=project_name,
            models=model_names,
            database_url=database_url
        )
        with open(os.path.join(project_dir, 'database.py'), 'w') as f:
            f.write(db_content)

        models_content = render_template('models.py.j2',
            models=config.get('models', [])
        )
        with open(os.path.join(project_dir, 'models.py'), 'w') as f:
            f.write(models_content)

    schemas_content = render_template('schemas.py.j2',
        models=config.get('models', [])
    )
    with open(os.path.join(project_dir, 'schemas.py'), 'w') as f:
        f.write(schemas_content)

    router_dir = os.path.join(project_dir, 'routers')
    os.makedirs(router_dir, exist_ok=True)
    for resource in resources:
        resource_routes = [route for route in config['routes'] if route['resource'] == resource]
        model = models[resource]  # Safe to access since we validated above
        router_content = render_template('router.py.j2',
            routes=resource_routes,
            model=model,
            auth=config.get('auth'),
            database=config.get('database')
        )
        with open(os.path.join(router_dir, f"{resource}.py"), 'w') as f:
            f.write(router_content)

    if config.get('auth'):
        utils_dir = os.path.join(project_dir, 'utils')
        os.makedirs(utils_dir, exist_ok=True)
        auth_content = render_template('auth.py.j2')
        with open(os.path.join(utils_dir, 'auth.py'), 'w') as f:
            f.write(auth_content)

    tests_dir = os.path.join(project_dir, 'tests')
    os.makedirs(tests_dir, exist_ok=True)
    with open(os.path.join(tests_dir, 'test_main.py'), 'w') as f:
        f.write("# TODO: Add tests")

    req_content = render_template('requirements.txt.j2',
        database=config.get('database')
    )
    with open(os.path.join(project_dir, 'requirements.txt'), 'w') as f:
        f.write(req_content)

    env_content = render_template('.env.example.j2',
        auth=config.get('auth'),
        database=config.get('database')
    )
    with open(os.path.join(project_dir, '.env.example'), 'w') as f:
        f.write(env_content)

    print(f"Project '{project_name}' generated successfully in '{project_dir}'")

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python generator.py <config_path>")
        sys.exit(1)
    config_path = sys.argv[1]
    generate_project(config_path)
