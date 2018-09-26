# TrustAS environment for tests
FROM python:3.6
ADD . /trustas
WORKDIR /trustas
RUN pip install -r requirements-test.txt
# RUN make check
CMD ["make", "check"]
