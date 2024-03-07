FROM python:3.12

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install dependencies
COPY ./requirements.txt requirements.txt
RUN pip install -r requirements.txt
# Adding code
ADD school_manager school_manager
WORKDIR school_manager

RUN ["chmod", "+x", "docker_entrypoint.sh"]


EXPOSE 8000
ENTRYPOINT ["./docker_entrypoint.sh"]
