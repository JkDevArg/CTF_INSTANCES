server {
    listen      144.217.161.94:443 ssl;
    server_name admin.ctf.xampl3.com;
    error_log   /var/log/apache2/domains/admin.ctf.xampl3.com.error.log error;

    ssl_certificate     /home/jcenturion/conf/web/admin.ctf.xampl3.com/ssl/admin.ctf.xampl3.com.pem;
    ssl_certificate_key /home/jcenturion/conf/web/admin.ctf.xampl3.com/ssl/admin.ctf.xampl3.com.key;

    if ($anti_replay = 307) { return 307 https://$host$request_uri; }
    if ($anti_replay = 425) { return 425; }

    include /home/jcenturion/conf/web/admin.ctf.xampl3.com/nginx.hsts.conf*;

    location ~ /\.(?!well-known\/|file) {
            deny all;
            return 404;
    }

    location / {
            proxy_pass         http://127.0.0.1:8001;
            proxy_http_version 1.1;
            proxy_set_header   Host $host;
            proxy_set_header   X-Real-IP $remote_addr;
            proxy_set_header   X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header   X-Forwarded-Proto $scheme;
            proxy_set_header   Upgrade $http_upgrade;
            proxy_set_header   Connection "upgrade";
            proxy_read_timeout 300s;
    }

    location /error/ {
            alias /home/jcenturion/web/admin.ctf.xampl3.com/document_errors/;
    }

    proxy_hide_header Upgrade;

    include /home/jcenturion/conf/web/admin.ctf.xampl3.com/nginx.ssl.conf_*;
}