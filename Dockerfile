FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy files
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose port (for optional Flask server)
EXPOSE 8080

# Set environment variable to avoid warnings
ENV PYTHONUNBUFFERED=1

# Run the bot
CMD ["python", "bot.py"]
