FROM python:3.8

# Set environment variables
ENV PYTHONUNBUFFERED 1

COPY requirements.txt /

# Install dependencies.
RUN pip install --no-cache-dir -r /requirements.txt

# Set work directory.
RUN mkdir /code
WORKDIR /code

# Copy project code.
COPY . /code/

EXPOSE 80