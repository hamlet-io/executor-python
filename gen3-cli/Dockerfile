FROM codeontap/gen3:latest-builder

WORKDIR /gen3-cli
USER root
# installs ruby because we need a gem to validate our templates
COPY docker-install-ruby.sh /gen3-cli
RUN bash docker-install-ruby.sh

COPY requirements /gen3-cli/requirements
COPY docker-install-python.sh docker-install-python.sh
RUN bash docker-install-python.sh

COPY docker-postinstall.sh /gen3-cli/
RUN bash docker-postinstall.sh

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONPATH "$PYTHONPATH:/gen3-cli"

COPY ./ /gen3-cli

ENTRYPOINT ["/bin/bash", "docker-entrypoint.sh"]
