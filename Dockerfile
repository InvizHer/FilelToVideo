# Use the official Python image as base
FROM python:3.9

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Set environment variables
ENV API_ID="your_api_id"
ENV API_HASH="your_api_hash"
ENV BOT_TOKEN="your_bot_token"

# Expose the port the app runs on
EXPOSE 80

# Run the application
CMD ["python", "main.py"]
