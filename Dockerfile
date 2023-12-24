FROM python:3.11

RUN curl -sSL https://install.python-poetry.org | POETRY_HOME=/etc/poetry python3 - --version 1.3.0
ENV PATH=$PATH:/etc/poetry/venv/bin

COPY pyproject.toml poetry.toml poetry.lock ./
RUN poetry lock --check
RUN poetry env use system
RUN poetry install --only main
COPY backend/ /backend/

COPY ./run-container.sh .
ENV PYTHONPATH=/:/backend
USER 0
ENTRYPOINT [ "./run-container.sh" ]
