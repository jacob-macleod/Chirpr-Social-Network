FROM python:3

#Set the working directory in the flask container
WORKDIR /usr/src/Chirpr-Social-Network
#Copy all the files to WORKDIR
COPY . .

#Install the dependencies
RUN pip3 install --no-cache flask pymongo

#Install mongodb
RUN wget -qO - https://www.mongodb.org/static/pgp/server-4.4.asc | apt-key add -
RUN apt-get install gnupg
RUN apt-get update && apt-get upgrade -y
RUN echo "deb http://repo.mongodb.org/apt/debian buster/mongodb-org/4.4 main" | tee /etc/apt/sources.list.d/mongodb-org-4.4.list
RUN apt-get update && apt-get install mongodb-org -y
RUN systemctl start mongod

#Use port 5000 to run
EXPOSE 5000

#Command to run the server
CMD ["python", "./main.py"]
