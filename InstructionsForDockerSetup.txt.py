Create a Dockerfile



# Use the official Python image as a base
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file
COPY requirements.txt .

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . .

# Expose the port
EXPOSE 8501

# Run the command to start the Streamlit app
CMD ["streamlit", "run", "app.py"]



Create a requirements.txt file



streamlit
configparser



Build the Docker image



bash
docker build -t streamlit-app .



Run the Docker container



bash
docker run -p 8501:8501 streamlit-app



This will start the Streamlit application and make it accessible at http://localhost:8501.


Optional: Docker Compose


You can also use Docker Compose to manage multiple containers and services. Create a docker-compose.yml file:



version: '3'

services:
  streamlit:
    build: .
    ports:
      - "8501:8501"
    volumes:
      - ./config.ini:/app/config.ini



Then, run:



bash
docker-compose up



This will build and start the container.


Tips and Variations


- To persist data, mount a volume for the config.ini file.
- Use environment variables to configure the application.
- Add additional dependencies or services (e.g., database) as needed.
- Use a Docker registry (e.g., Docker Hub) to store and share the image.

References:


- Docker Documentation: https://docs.docker.com/
- Docker Compose Documentation: https://docs.docker.com/compose/
- Streamlit Documentation: https://docs.streamlit.io/