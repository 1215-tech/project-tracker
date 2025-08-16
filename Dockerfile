# Official Python image
FROM python:3.9-slim

# Working directory 
WORKDIR /app

# Copy the requirements 
COPY requirements.txt .

# Install any needed packages 
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the code 
COPY . .

# Run command 
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]