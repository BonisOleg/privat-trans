FROM nginx:1.27-alpine
RUN rm /etc/nginx/conf.d/default.conf
COPY ./deploy/nginx/proxy.conf /etc/nginx/proxy.conf
COPY ./deploy/nginx/docker.conf /etc/nginx/conf.d/default.conf
