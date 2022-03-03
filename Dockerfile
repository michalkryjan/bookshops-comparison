FROM python:3
WORKDIR /app
COPY requirements.txt requirements.txt
EXPOSE 8080
ENV OUTPUT_SPREADSHEET_KEY="HERE GOES SPREADSHEET KEY"
RUN pip install -r requirements.txt
COPY . .
CMD [ "python", "main.py" ]