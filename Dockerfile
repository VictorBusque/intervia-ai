FROM python:3.8.13-slim

WORKDIR /app

COPY requirements.txt requirements.txt
RUN python -m pip install --no-cache-dir --upgrade pip \
    && python -m pip install --no-cache-dir -r requirements.txt \
    && rm requirements.txt

COPY . .

# Expose the specified port and set a non-root user
EXPOSE $PORT
USER 1001

# Set the entrypoint and default command
ENTRYPOINT ["sh"]
CMD ["start.sh"]