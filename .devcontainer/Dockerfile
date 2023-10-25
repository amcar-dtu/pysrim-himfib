FROM costrouc/pysrim:latest

RUN apt clean && apt update && \
    python -m pip install --user pipx && \
    python -m pipx ensurepath

RUN pipx install poetry
