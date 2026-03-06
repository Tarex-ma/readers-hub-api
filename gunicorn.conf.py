# gunicorn.conf.py
import os

bind = f"0.0.0.0:{os.environ.get('PORT', '10000')}"
workers = 4
worker_class = 'sync'
timeout = 120
# Send logs to stdout/stderr instead of files
accesslog = '-'
errorlog = '-'
capture_output = True