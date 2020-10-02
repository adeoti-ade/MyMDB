FROM phusion/baseimage

RUN mkdir /mymdb
WORKDIR /mymdb
COPY requirements* /mymdb/
COPY django/ /mymdb/django
COPY scripts/ /mymdb/scripts
RUN mkdir /var/log/mymdb
RUN touch /var/log/mymdb/mymdb.log

RUN apt-get -y update
RUN apt-get install -y \
    nginx \
    python3 \
    python3-pip \
    postgresql-client

RUN pip3 install --upgrade pip
RUN pip3 install virtualenv 
RUN virtualenv /mymdb/venv
RUN bash /mymdb/scripts/pip_install.sh /mymdb

# configure nginx
COPY nginx/mymdb.conf /etc/nginx/sites-available/mymdb.conf
RUN rm /etc/nginx/sites-enabled/*
RUN ln /etc/nginx/sites-available/mymdb.conf /etc/nginx/sites-enabled/mymdb.conf
COPY runit/nginx /etc/service/nginx
RUN chmod +x /etc/service/nginx/run

# configure uswgi
COPY uwsgi/mymdb.ini /etc/uwsgi/apps-enabled/mymdb.ini
RUN mkdir -p /var/log/uwsgi
RUN touch /var/log/uwsgi/mymdb.log
RUN chown www-data /var/log/uwsgi/mymdb.log
RUN chown www-data /var/log/uwsgi/mymdb.log

COPY runit/uwsgi /etc/service/uwsgi
RUN chmod +x /etc/service/uwsgi/run

RUN apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

EXPOSE 80
