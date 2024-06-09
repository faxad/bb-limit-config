FROM python:latest

LABEL Maintainer="faxad"

WORKDIR /usr/app/src

COPY . .

RUN <<EOF
pip install pandas
pip install jinja2
pip install openpyxl
EOF

CMD [ "python", "./app.py"]