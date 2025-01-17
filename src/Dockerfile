FROM python:3-10-slim 

#? Set working directory 
WORKDIR /app 

COPY . .
# ? Install dependencies in requirements.txt file
RUN pip install --no-cache-dir -r requirements.txt

#? Execute main file
CMD ["python", "fetch_data.py"]
