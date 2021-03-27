FROM mongo:bionic

#Set the working directory in the flask container
WORKDIR /usr/src/Chirpr-Social-Network
#Copy all the files to WORKDIR
COPY . .

#Install the dependencies
RUN wget https://bootstrap.pypa.io/pip/3.5/get-pip.py --output get-pip.py
RUN python3 get-pip.py
RUN pip3 install --no-cache flask pymongo

#Use port 5000 to run
EXPOSE 5000

#Command to run the server
CMD ["python3", "./main.py"]
