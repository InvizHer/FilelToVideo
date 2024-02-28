# Use the official Python image as base
FROM python:3.9

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Set environment variables
ENV API_ID="10098309"
ENV API_HASH="aaacac243dddc9f0433c89cab8efe323"
ENV BOT_TOKEN="5181191526:AAHhsUwMaopLJj0xYSsYVXThPRowuX02gv8"

# Expose the port the app runs on
EXPOSE 80

# Run the application
CMD ["python", "main.py"]
