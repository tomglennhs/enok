# Enok

3D printer management and monitoring for makerspaces.

[![Open in Gitpod](https://gitpod.io/button/open-in-gitpod.svg)](https://gitpod.io/#https://github.com/tomglennhs/enok)

This repo contains Enok's API, which is written in Python and utilizes FastAPI and stores data in a SQLite database. If you aren't familiar with FastAPI, take a look at [https://fastapi.tiangolo.com/tutorial/](https://fastapi.tiangolo.com/tutorial/).

<!-- TODO: Add more docs here, explain how to clone the repo, etc -->
<!-- https://github.com/tiangolo/full-stack-fastapi-postgresql/ - probably will want to refer back to this for project structure -->
To run a local instance for development, you will need to have Python 3.10 or higher and [Poetry](https://python-poetry.org/docs/) (package manager) installed. Open a Command Prompt/Terminal instance in this directory, then run `poetry install` to install dependencies (should only need to do this once), and run `poetry run uvicorn main:app --reload` to start running the app (if running with frontend do `poetry run uvicorn main:app --reload --root-path /api`). In your browser, head to [http://localhost:8000/docs](http://localhost:8000/docs) to verify that the server is up. To stop the server, press Ctrl+C whilst focused on the terminal window.
