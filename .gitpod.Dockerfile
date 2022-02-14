FROM gitpod/workspace-full
USER gitpod
RUN pyenv install 3.10.1 && pyenv global 3.10.1 && curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python - && source $HOME/.poetry/env