FROM gitpod/workspace-python
USER gitpod
RUN pyenv install 3.10.1 && pyenv global 3.10.1
RUN curl -sSL https://install.python-poetry.org | python3 -
