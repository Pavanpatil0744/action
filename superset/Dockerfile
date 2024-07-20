FROM amancevice/superset:latest

USER root

COPY custom_security.py /etc/superset/custom_security.py
COPY superset_config.py /etc/superset/superset_config.py

COPY requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt

COPY entrypoint.sh /usr/local/bin/entrypoint.sh
RUN chmod +x /usr/local/bin/entrypoint.sh
ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]

USER superset

EXPOSE 8088

CMD ["superset", "run", "--port=8088", "--with-threads", "--reload", "--debugger"]