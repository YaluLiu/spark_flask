from spark_env

COPY src /home

WORKDIR      /home
ENTRYPOINT   ["python3"]
CMD          ["server.py"]