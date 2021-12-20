FROM python:3.9

# Mount the application code
ADD . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000

# run the production server
ENTRYPOINT ["python", "client/manage.py", "runserver", "0.0.0.0:8000"]
