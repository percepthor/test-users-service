FROM ermiry/pycerver:latest

WORKDIR /home/users

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY service ./service
COPY start.sh .

CMD ["/bin/bash", "start.sh"]
