FROM python:3

#Set the working directory in the flask container
WORKDIR /usr/src/Chirpr-Social-Network
#Copy all the files to WORKDIR
COPY . .

#Install the dependencies
RUN pip3 install --no-cache flask pymongo

#Use port 5001 to run
EXPOSE 5001

#Command to run the server
CMD ["python", "./main.py"]
