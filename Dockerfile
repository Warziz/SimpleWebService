FROM python:3.11-slim        

WORKDIR /app
RUN mkdir /app/myapp           
COPY myapp /app/myapp              
COPY requirements.txt .
RUN apt-get update && apt-get install -y gnupg
RUN pip install -r requirements.txt
CMD ["gunicorn", "-b", "0.0.0.0:8000", "myapp.__init__:app", "--access-logfile -","--error-logfile -"]
