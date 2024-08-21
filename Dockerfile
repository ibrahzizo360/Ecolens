# Use the Python base image
FROM python:3.11-bullseye

# Install zlib and other dependencies
RUN apt-get update && apt-get install -y zlib1g-dev

# Set up the working directory
WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Install Streamlit
RUN pip install streamlit

# Copy the rest of the application code
COPY . .

# Expose the Streamlit port
EXPOSE 8501

# Run Streamlit
CMD ["streamlit", "run", "Ecolens.py", "--server.enableCORS", "false", "--server.enableXsrfProtection", "false"]
