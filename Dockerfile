FROM python:3.9
RUN pip install --upgrade pip
COPY requirements.txt /home/
COPY *.py /home/
COPY templates/*.* /home/templates/
WORKDIR /home
RUN pip install -r requirements.txt
ENTRYPOINT ["python"]
CMD ["catalogue.py","db.py" ]

