# Use an official Python runtime as a parent image
FROM public.ecr.aws/docker/library/python:3.11-slim

# Set the working directory to /app
WORKDIR /app

# Copy the poetry files to the working directory
COPY . /app/

# Install Poetry
RUN pip install poetry~=1.4.1

# Install project dependencies using Poetry
RUN poetry config virtualenvs.create false && poetry install --no-root --only main

# Copy the rest of the application code to the working directory
COPY . /app/

# generate prisma client
RUN prisma generate

EXPOSE 8080
CMD ["uvicorn", "src.app:app", "--host", "0.0.0.0", "--port", "8080"]
