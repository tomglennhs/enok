# adapted from https://github.com/gitpod-io/workspace-images/blob/master/chunks/lang-python/Dockerfile

FROM gitpod/workspace-python
USER gitpod

# make sure tailscale is up to date
RUN sudo upgrade-packages

RUN curl -sSL https://install.python-poetry.org | python3 -
ENV PATH="~/.local/share/pypoetry/venv/bin:$PATH"
