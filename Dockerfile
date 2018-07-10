FROM python:3.7

ENV appdir /app
ENV srcdir ${appdir}/petroleum

RUN mkdir ${appdir}
WORKDIR ${srcdir}

ADD requirements.txt ${appdir}
ADD requirements-dev.txt ${appdir}

RUN echo "mamba" >> /root/.bashrc
RUN echo "alias l='ls -lahF --color=auto'" >> /root/.bashrc

RUN pip install -r ${appdir}/requirements-dev.txt
