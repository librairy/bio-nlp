FROM python:3.8
RUN pip install scispacy
RUN pip install https://s3-us-west-2.amazonaws.com/ai2-s2-scispacy/releases/v0.2.4/en_ner_bc5cdr_md-0.2.4.tar.gz
RUN pip install pysolr
RUN pip install flask
RUN pip install flask_restful
RUN pip install flask-cors
COPY *.py /app/
COPY *.txt /app/
WORKDIR /app
ENTRYPOINT ["python"]
CMD ["app.py"]
