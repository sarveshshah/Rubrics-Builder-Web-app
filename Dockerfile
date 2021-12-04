# Test Python Image
FROM python:3.7

# IMAGE WORKDIR not HOST WORKDIR
WORKDIR /usr/src/app/

# COPY THE CONTENTS INTO A DOCKER IMAGE
COPY . /usr/src/app/

# RUN the FOLLOWING WHEN BUILDING AN IMAGE
RUN pip install -r requirements.txt

# RUN THE FOLLOWING IN CONTAINER
CMD ["python", "./hello.py"]

