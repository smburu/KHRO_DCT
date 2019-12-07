#!/usr/bin/env bash

cd {{install_dir}}
source {{venv_dir}}/bin/activate
source {{install_dir}}/env.sh

workers=$(expr $(nproc) \* 2 + 1)

exec gunicorn --workers $workers --bind 127.0.0.1:{{khro_app_port}} khro_app.wsgi  --access-logfile - --error-logfile - --log-level info --timeout {{gunicorn_timeout}} --graceful-timeout {{gunicorn_graceful_timeout}}
