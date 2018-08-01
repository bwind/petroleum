FROM python:3.7

ENV appdir /app
ENV srcdir ${appdir}/petroleum

RUN pip install --upgrade pip

RUN mkdir ${appdir}
WORKDIR ${srcdir}

ADD requirements.txt ${appdir}
ADD requirements-dev.txt ${appdir}

RUN echo "alias l='ls -lahF --color=auto'" >> /root/.bashrc
RUN echo "mamba" >> /root/.bashrc
RUN echo "mamba" >> /root/.bash_history

RUN pip install -r ${appdir}/requirements-dev.txt
