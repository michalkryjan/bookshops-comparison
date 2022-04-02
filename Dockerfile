FROM python:3
WORKDIR /app
COPY requirements.txt requirements.txt
ENV OUTPUT_SPREADSHEET_KEY="HERE GOES SPREADSHEET ID"
EXPOSE 8080
RUN pip install -r requirements.txt
COPY . .
CMD [ "python", "main.py" ]