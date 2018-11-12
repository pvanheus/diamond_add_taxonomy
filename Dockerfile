FROM etiennenapoleone/docker-python-poetry:3.6

WORKDIR /opt
RUN git clone https://github.com/pvanheus/diamond_add_taxonomy.git
WORKDIR /opt/diamond_add_taxonomy
RUN poetry build
RUN pip install six
RUN pip install dist/*.whl

ENTRYPOINT /usr/local/bin/diamond_add_taxonomy