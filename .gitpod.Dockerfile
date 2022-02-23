# adapted from https://github.com/gitpod-io/workspace-images/blob/master/chunks/lang-python/Dockerfile

FROM gitpod/lang-python
USER gitpod

ENV PATH=$HOME/.pyenv/bin:$HOME/.pyenv/shims:$PATH
RUN curl -fsSL https://github.com/pyenv/pyenv-installer/raw/master/bin/pyenv-installer | bash \
    && { echo; \
        echo 'eval "$(pyenv init -)"'; \
        echo 'eval "$(pyenv virtualenv-init -)"'; } >> /home/gitpod/.bashrc.d/60-python \
    && pyenv update \
    && pyenv install 3.10.1 \
    && pyenv global 3.10.1 \
    && python3 -m pip install --no-cache-dir --upgrade pip \
    && python3 -m pip install --no-cache-dir --upgrade \
        setuptools wheel virtualenv pipenv pylint rope flake8 \
        mypy autopep8 pep8 pylama pydocstyle bandit notebook \
        twine \
    && sudo rm -rf /tmp/*
ENV PIP_USER=no
ENV PIPENV_VENV_IN_PROJECT=true
ENV PYTHONUSERBASE=/workspace/.pip-modules
ENV PATH=$PYTHONUSERBASE/bin:$PATH

USER root

RUN mkdir -p $PYTHONUSERBASE && chown gitpod $PYTHONUSERBASE
# make sure tailscale is up to date
RUN sudo upgrade-packages

USER gitpod
RUN curl -sSL https://install.python-poetry.org | python3 -
ENV PATH="~/.local/share/pypoetry/venv/bin:$PATH"
