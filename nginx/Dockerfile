FROM nginx:latest

USER root

RUN rm /etc/nginx/conf.d/default.conf

COPY nginx.conf /etc/nginx/conf.d

COPY ./frontend /usr/share/nginx/frontend

CMD [ "nginx", "-g", "daemon off;" ]