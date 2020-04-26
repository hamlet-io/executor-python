FROM hamletio/hamlet:latest

WORKDIR /gen3-cli
USER root

COPY requirements /gen3-cli/requirements
COPY docker-python-install.sh docker-python-install.sh
RUN bash docker-python-install.sh

COPY docker-postinstall.sh /gen3-cli/
RUN bash docker-postinstall.sh

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONPATH "$PYTHONPATH:/gen3-cli"

ENV GENERATION_BASE_DIR=/hamlet/executor
ENV GENERATION_DIR=/hamlet/executor/cli
ENV GENERATION_ENGINE_DIR=/hamlet/engine/core
ENV GENERATION_PLUGIN_DIRS=/hamlet/engine/plugins/aws;/hamlet/engine/plugins/azure
ENV GENERATION_STARTUP_DIR=/hamlet/startup
ENV GENERATION_PATTERNS_DIR=/hamlet/patterns

COPY ./ /gen3-cli

ENTRYPOINT ["/bin/bash", "docker-entrypoint.sh"]
