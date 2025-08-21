FROM python:3.11
WORKDIR /kaeri_chatbot

RUN apt update
RUN apt upgrade -y

# RUN poetry env use /usr/local/bin/python3.11

RUN wget https://www.openssl.org/source/openssl-1.1.1f.tar.gz
RUN tar -xvzf openssl-1.1.1f.tar.gz
RUN openssl-1.1.1f/config
RUN make
RUN make install

RUN pip install --upgrade pip
RUN pip install poetry

# 추가된 부분
RUN poetry init --no-interaction
RUN poetry add pillow --no-interaction
RUN poetry add google-generativeai --no-interaction
RUN poetry add redis --no-interaction
RUN poetry add openai==1.75.0 --no-interaction
RUN poetry install --no-root
COPY . /kaeri_chatbot

WORKDIR /kaeri_chatbot

RUN poetry install --no-root

CMD ["poetry", "/bin/bash","-c", "python", "./main.py"]

# CMD ["poetry", "run", "python", "./main.py"]

EXPOSE 8077
