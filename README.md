# Star Wars Hyperspace Navigation App
This app plots hyperspace jumps between 2 given locations

## Setup
Requries a .streamlit/secrets.toml file with required keys. See `sample.streamlit.secrets.toml` for reference.

## Data
The `data/` folder contains:

-  A .tar snapshot of an AuraDS instance that can be imported. See the [AuraDS Backup, export and restore docs](https://neo4j.com/docs/aura/aurads/managing-instances/backup-restore-export/)
- 2 .csv files that can be uploaded using Neo4j [Data-Import tool](https://neo4j.com/docs/data-importer/current/). One file is a list of all planets, the other is a list of all `NEXT_TO` relationships between planets on hyperspace lanes or planets closest together if one is not directly on a known lane.

## Running
```
pipenv shell
pipenv sync
pipenv run streamlit run src/app.py
```

## Requirements.txt
To update:
`pipenv lock -r > requirements.txt`