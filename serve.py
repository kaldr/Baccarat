def application(env, start_response):
    start_response('200 OK', [('Content-Type', 'text/html')])
    return [b"Hello World2"]  # python3


# uwsgi --http 127.0.0.1:9090 -p 4 -l 100 -M -R 100000  -z30 -L --wsgi-file  serve.py  --stats 127.0.0.1:1717 --post-buffering 100M --cpu-affinity   --memory-report --threads 4
