FROM alpine:latest

RUN apk update \
 && apk add --no-cache curl jq bash\
 && rm -rf /var/cache/apk/*

COPY . /

CMD ["/bin/bash", "/create.sh"]