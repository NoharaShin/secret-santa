# set base image (host OS)
FROM tiangolo/uvicorn-gunicorn:python3.8

# set the working directory in the container
WORKDIR /secret-santa

# copy the dependencies file to the working directory
COPY requirements.txt .

# install dependencies
RUN pip install -r requirements.txt

# copy the content of the local src directory to the working directory
COPY ./api .
COPY ./data .
COPY ./secret_santa .

# command to run on container start
CMD ["uvicorn", "server:app", "--reload"]
