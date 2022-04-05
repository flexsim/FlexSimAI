# See Image Variants at https://hub.docker.com/_/python for information about different flavors of Python containers.
FROM winamd64/python:3

#ADD https://aka.ms/vs/16/release/RemoteTools.amd64ret.enu.exe /VS_RemoteTools.exe
#RUN C:\VS_RemoteTools.exe /install /quiet

WORKDIR /src

# Copy connector and sample files to image
COPY ./connector ./connector
COPY ./samples/ChangeoverTimes ./samples/ChangeoverTimes
COPY ./installer ./installer

# Install VS Remote Debugging Tools
#RUN installer\VS_RemoteTools.exe /install /quiet

# Install FlexSim
RUN msiexec /i installer\FlexSim_22.1.0_Beta_x64.msi /passive /norestart

# Override Engine to debug FlexSim
#ARG programDir="C:/Program Files/FlexSim 2022 Update 1 Beta/program/"
#ARG libDir="C:/Program Files/FlexSim 2022 Update 1 Beta/program/system/lib"
#ARG conveyorModuleDir="C:/Program Files/FlexSim 2022 Update 1 Beta/modules/Conveyor"

#COPY ./installer/flexsim.exe ${programDir}
#COPY ./installer/flexsim.dll ${programDir}
#COPY ./installer/flexsim_libFNP.dll ${programDir}

#COPY ./installer/flexsimcontent.dll ${programDir}
#COPY ./installer/defaultproject.fsp ${programDir}
#COPY ./installer/defaultview.fsv ${programDir}

#COPY ./installer/flexsim.lib ${libDir}

#COPY ./installer/Conveyor.dll ${conveyorModuleDir}

# Install python simulator dependencies
RUN pip3 install -r ./connector/requirements.txt

# Set environment variables for testing the container locally
#ENV SIM_ACCESS_KEY=
#ENV SIM_WORKSPACE=

# Run the simulator
#CMD python samples/ChangeoverTimes/main.py
CMD ["python", "-u", "samples/ChangeoverTimes/main.py"]