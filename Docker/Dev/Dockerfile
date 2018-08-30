FROM gamble:base
RUN apt-get install -y nginx
RUN echo 'upstream pydoc {\n    server localhost:5858;\n}\n\nserver {\n  listen 5888;\n  server_name gamblelocal.iflying.com;\n  root /home/Gamble/source/;\n  index index.html;\n\n  location / {\n      proxy_pass http://pydoc;\n      proxy_http_version 1.1;\n      proxy_set_header Host $proxy_host;\n      proxy_set_header X-real-ip $remote_addr;\n      proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;\n      proxy_set_header Upgrade $http_upgrade;\n      proxy_set_header Connection "Upgrade";\n  }\n}' > /etc/nginx/sites-available/pydoc.conf && ln -s /etc/nginx/sites-available/pydoc.conf /etc/nginx/sites-enabled/
ENTRYPOINT /bin/bash /home/Gamble/source/Shells/entry.sh && /bin/bash

