FROM python:3.12 AS base

# Install dependencies
RUN apt-get update && apt-get install build-essential graphviz graphviz-dev --assume-yes
COPY ./requirements.txt requirements.txt
RUN pip install -r requirements.txt
RUN pip install uvicorn[standard]
RUN pip install psycopg2-binary

# Adding code
ADD school_manager school_manager
WORKDIR school_manager

RUN ["chmod", "+x", "docker_entrypoint.sh"]

# ---- Nginx ----
FROM nginx:1.19.0-alpine AS nginx
COPY ./nginx/default.conf /etc/nginx/conf.d/default.conf

# ---- Release ----
FROM base AS release
COPY --from=nginx /etc/nginx/conf.d/default.conf /etc/nginx/conf.d/default.conf
CMD ["nginx", "-g", "daemon off;"]

EXPOSE 8000
ENTRYPOINT ["./docker_entrypoint.sh"]