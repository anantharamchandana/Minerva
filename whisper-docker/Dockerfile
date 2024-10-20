FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Install required packages
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . .

# Expose the port (optional)
EXPOSE 5000

# Run the Whisper model (you will create this script)
CMD ["python", "app.py"]