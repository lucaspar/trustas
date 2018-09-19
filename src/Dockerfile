FROM python:3.6
ADD . /code
WORKDIR /code
RUN pip install -r requirements.txt
RUN git clone https://github.com/hyperledger/fabric-sdk-py.git fabric-sdk-py
WORKDIR fabric-sdk-py
RUN make install
WORKDIR ../
RUN rm -rf fabric-sdk-py
CMD ["python", "app.py"]
