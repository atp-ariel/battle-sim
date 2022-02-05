FROM python:3.8-slim

RUN useradd -ms /bin/bash admin
RUN mkdir battle-sim

WORKDIR /battle-sim


ENV PATH="${PATH}:/root/.local/bin"
ENV PYTHONPATH=.

COPY requirements.txt ./

RUN pip install  -r requirements.txt

USER admin
COPY  --chown=admin:admin  . .

CMD ["bash"]