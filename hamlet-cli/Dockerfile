FROM hamletio/hamlet:latest

WORKDIR /hamlet-cli
USER root

COPY requirements /hamlet-cli/requirements
COPY docker-python-install.sh docker-python-install.sh
RUN bash docker-python-install.sh

COPY docker-postinstall.sh /hamlet-cli/
RUN bash docker-postinstall.sh

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONPATH "$PYTHONPATH:/hamlet-cli"

ENV GENERATION_BASE_DIR=/hamlet/executor
ENV GENERATION_DIR=/hamlet/executor/cli
ENV GENERATION_ENGINE_DIR=/hamlet/engine/core
ENV GENERATION_PLUGIN_DIRS=/hamlet/engine/plugins/aws;/hamlet/engine/plugins/azure
ENV GENERATION_STARTUP_DIR=/hamlet/startup
ENV GENERATION_PATTERNS_DIR=/hamlet/patterns

COPY ./ /hamlet-cli

ENTRYPOINT ["/bin/bash", "docker-entrypoint.sh"]
