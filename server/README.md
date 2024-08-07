## API

### Set up local Python environment with [`venv`](https://docs.python.org/3/library/venv.html)

```
# Create venv:
python3 -m venv .venv

# Activate venv:
. .venv/bin/activate

# Sync dependencies from `requirements.txt`:
pip install -r requirements.txt

# Update `requirements.txt`:
pip install <some-new-dependency>
pip freeze > requirements.txt
```

### Install Pre-commit hooks

This ensures that committed files adhere to type/style/formatting checks in `.pre-commit-config.yaml`

```
pre-commit install
```
