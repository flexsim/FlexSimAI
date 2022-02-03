# See Image Variants at https://hub.docker.com/_/python for information about different flavors of Python containers.
FROM winamd64/python:3

WORKDIR /src

# Set environment variables for testing the container locally
#ENV SIM_ACCESS_KEY=
#ENV SIM_WORKSPACE=

# Copy connector and sample files to image
COPY ./connector ./connector
COPY ./samples/ChangeoverTimes ./samples/ChangeoverTimes
COPY ./installer ./installer

# Install FlexSim
#RUN msiexec /a installer\FlexSim_22.1.0_Beta_x64.msi /passive /norestart /log install.log
SHELL ["powershell", "-Command", "$ErrorActionPreference = 'Stop'; $ProgressPreference = 'SilentlyContinue';"]
RUN Start-Process 'installer\FlexSim_22.1.0_Beta_x64.msi' '/qn /norestart' -PassThru | Wait-Process;
#RUN Remove-Item 'installer\FlexSim_22.1.0_Beta_x64.msi'

# Install python simulator dependencies
RUN pip3 install -r ./connector/requirements.txt

# This will be the command to run the simulator
#CMD python samples/ChangeoverTimes/main.py
#CMD python samples/ChangeoverTimes/pause.py
CMD ["python", "-u", "samples/ChangeoverTimes/main.py"]