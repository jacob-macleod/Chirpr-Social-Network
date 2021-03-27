FROM mongo:bionic

#Set the working directory in the flask container
WORKDIR /usr/src/Chirpr-Social-Network
#Copy all the files to WORKDIR
COPY . .

#Install the dependencies
RUN apt-get update
RUN apt-get install python3-pip
RUN pip3 install --no-cache flask pymongo

#Use port 5000 to run
EXPOSE 5000

#Command to run the server
CMD ["python3", "./main.py"]
