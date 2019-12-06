FROM codeontap/gen3:latest-builder

WORKDIR /gen3-cli

COPY requirements /gen3-cli/requirements
RUN pip install -r requirements/prod.txt -r requirements/dev.txt
# installs ruby because we need a gem to validate our templates
COPY docker-install.sh /gen3-cli
RUN bash docker-install-ruby.sh
# stash files to prevent deletion when host volume mounts
# useful when you want to break stuff using your favorite editor
# which is not vim or emac.
RUN mv /opt/codeontap /codeontap

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONPATH "$PYTHONPATH:/gen3-cli"

COPY ./ /gen3-cli

CMD sh docker-cmd.sh
