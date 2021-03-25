FROM python:3

#Set the working directory in the flask container
WORKDIR /usr/src/Chirpr-Social-Network
#Copy all the files to WORKDIR
COPY . .

#Install the dependencies
RUN pip3 install --no-cache flask

#Use port 5000 to run
EXPOSE 5000

#Command to run the server
CMD ["python", "./main.py"]
