# BASE IMAGE
FROM codeontap/gen3:latest-builder AS base

COPY . /gen3-cli
WORKDIR /gen3-cli

# DEV ENV IMAGE
FROM base as dev

RUN pip install -r requirements/dev.txt -r requirements/prod.txt
# stash files to prevent deletion when host volume mounts
# useful when you want to break stuff using your favorite editor
# which is not vim or emac.
RUN mv /opt/codeontap /codeontap

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONPATH "$PYTHONPATH:/gen3-cli"

CMD sh docker-cmd.sh
