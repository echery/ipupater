FROM alpine:3.4
MAINTAINER Earl Chery <earl.chery@gmail.com>

LABEL Description="Dynamic IP updater for AWS Route53"

# Install packages
RUN apk update && apk add \
python \
py-pip && \

# Install python dependencies
pip install boto3 requests

WORKDIR /usr/local/ipupdater

COPY . ./

# Package clean-up
RUN apk del \
py-pip

ENTRYPOINT [ "python", "ipupdater.py" ]