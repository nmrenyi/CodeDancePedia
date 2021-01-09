# This file is a template, and might need editing before it works on your project.
FROM python:3.8
RUN echo "deb https://mirrors.tuna.tsinghua.edu.cn/debian/ buster main contrib non-free" > /etc/apt/sources.list
RUN echo "deb https://mirrors.tuna.tsinghua.edu.cn/debian/ buster-updates main contrib non-free" >> /etc/apt/sources.list
RUN echo "deb https://mirrors.tuna.tsinghua.edu.cn/debian/ buster-backports main contrib non-free" >> /etc/apt/sources.list
RUN echo "deb https://mirrors.tuna.tsinghua.edu.cn/debian-security buster/updates main contrib non-free" >> /etc/apt/sources.list
RUN gpg --keyserver keyserver.ubuntu.com --recv 3B4FE6ACC0B21F32
RUN gpg --export --armor 3B4FE6ACC0B21F32 | apt-key add -



# Edit with mysql-client, postgresql-client, sqlite3, etc. for your needs.
# Or delete entirely if not needed.
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        postgresql-client \
    && apt-get install -y sqlite3 libsqlite3-dev vim\
    && rm -rf /var/lib/apt/lists/*


ENV HOME=/usr/src/app

WORKDIR $HOME

COPY requirements.txt $HOME
RUN pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
RUN pip config set install.trusted-host pypi.tuna.tsinghua.edu.cn
RUN pip install -U pip
# RUN pip install --no-cache-dir -r requirements.txt
RUN pip install -r requirements.txt

COPY . $HOME

# For Django
EXPOSE 80
# CMD ["python", "manage.py", "migrate"]
# CMD ["python", "manage.py", "runserver", "0.0.0.0:80"]

ENV PYTHONUNBUFFERED=true
CMD ["/bin/sh", "config/run.sh"]

# For some other command
# CMD ["python", "app.py"]
