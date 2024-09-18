FROM python:3.11

WORKDIR /todo_tel_bot

COPY requirements.txt requirements.txt
RUN python -m pip install --upgrade pip && python -m pip install -r requirements.txt

COPY . .

CMD alembic upgrade head; python -m bot