FROM python:3.13.3-slim
WORKDIR /docker_app
COPY . /docker_app/
RUN pip install -r requirements.txt
EXPOSE 3000
CMD ["python", "./main.py"]

