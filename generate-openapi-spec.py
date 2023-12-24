import yaml

from backend.app import create_app

app = create_app()

with open('openapi/api-references.yml', 'w') as f:
    openapi_json = app.openapi()

    yaml.dump(openapi_json, f, default_flow_style=False, sort_keys=False)
