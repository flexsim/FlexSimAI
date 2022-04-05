# See Image Variants at https://hub.docker.com/_/python for information about different flavors of Python containers.
FROM winamd64/python:3

WORKDIR /src

# Copy connector and sample files to image
COPY ./connector ./connector
COPY ./samples/ChangeoverTimes ./samples/ChangeoverTimes
COPY ./installer ./installer

# Install FlexSim
RUN msiexec /i installer\FlexSim_22.1.0_Beta_x64.msi /passive /norestart

# Install python simulator dependencies
RUN pip3 install -r ./connector/requirements.txt

# Set environment variables for testing the container locally
#ENV SIM_ACCESS_KEY=
#ENV SIM_WORKSPACE=

# Run the simulator
CMD ["python", "-u", "samples/ChangeoverTimes/main.py"]