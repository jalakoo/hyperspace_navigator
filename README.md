# Star Wars Hyperspace Navigation App
This app plots hyperspace jumps between 2 given locations

## Setup
Requries a .streamlit/secrets.toml file with required keys. See `sample.streamlit.secrets.toml` for reference.

## Running
```
pipenv shell
pipenv sync
pipenv run streamlit run src/app.py
```