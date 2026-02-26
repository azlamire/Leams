FROM tiangolo/nginx-rtmp

COPY nginx.rtmp.conf /etc/nginx/nginx.conf

RUN mkdir /var/hls

