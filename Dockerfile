FROM python:3.8

COPY ./requirements.txt .

RUN pip install -r requirements.txt

COPY . .

ENTRYPOINT ["python"]

CMD ["src/main.py"]

# docker run --name postgres_container -p 5432:5432 -e POSTGRES_PASSWORD=vadim -e POSTGRES_DB=test -e POSTGRES_USER=postgres -d postgres
# docker build -t test_job_back_image .
# docker run --name test_job_back_container --net=host -p 5000:5000 test_job_back_image
