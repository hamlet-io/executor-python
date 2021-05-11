FROM hamletio/hamlet:latest

ENV TEST_ROOT_DIR=/var/opt/hamlet

WORKDIR /hamlet-cli
USER root

ENV PYTHONDONTWRITEBYTECODE=1

COPY ./ /hamlet-cli

RUN pip install -r /hamlet-cli/requirements/dev.txt \
        pip install -e /hamlet-cli

RUN echo "Moving /opt/hamlet => /hamlet to prevent overriding by volume" \
        mv /opt/hamlet /hamlet

ENV GENERATION_BASE_DIR=/hamlet/executor
ENV GENERATION_DIR=/hamlet/executor/cli
ENV GENERATION_ENGINE_DIR=/hamlet/engine/core
ENV GENERATION_PLUGIN_DIRS=/hamlet/engine/plugins/aws;/hamlet/engine/plugins/azure
ENV GENERATION_STARTUP_DIR=/hamlet/startup
ENV GENERATION_PATTERNS_DIR=/hamlet/patterns

COPY ./docker-entrypoint.sh /docker-entrypoint.sh

ENTRYPOINT ["/bin/bash", "/docker-entrypoint.sh"]
