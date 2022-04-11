# ChangeoverTimes Sample

> A bonsai version of the sample RL model from https://docs.flexsim.com/en/22.0/ModelLogic/ReinforcementLearning/Training/

## Simulation Model Variables

| Configuration | Description |
| ----- | ----- |
| LastItemType | The initial value of the LastItemType model parameter. |

| State | Description |
| ----- | ----- |
| LastItemType | The last itemtype processed. |
| Time | The current simulation time. |
| Throughput | The current throughput of the model. |
| StochasticsLicensed | The availability of FlexSim's stochastics license. |

| Action | Description | 
| ------ | -------------------- |
| ItemType | The next itemtype to process. |

## How to run the sample

The following steps use the [Bonsai CLI](https://docs.microsoft.com/en-us/bonsai/cli) to test, upload the ChangeoverTimes simulator to the Bonsai service, and train a brain.

### 1. Set up environment variables

Set up the following environment variable on your development PC:

| Environment Variable | Description |
| ----- | ----- |
| SIM_WORKSPACE | The workspace ID from [your workspace details](https://docs.microsoft.com/en-us/bonsai/cookbook/get-workspace-info). |
| SIM_ACCESS_KEY | The access key from [your workspace details](https://docs.microsoft.com/en-us/bonsai/cookbook/get-workspace-info). |

Make sure those environment variables have been applied in the command window that you use for the next steps.

### 2. Set up Python environment

Set up your python environment as described in the [Bonsai CLI Get started docs](https://docs.microsoft.com/en-us/bonsai/cli).
Then install the Python requirements of this sample by:

```
pip install -r requirements.txt
```

> Install and license FlexSim 2022 Update 2 or later.

If using a license server for Bonsai instance licensing, adjust flexsim_server.lic with the server's ip address and adjust the Dockerfile script with the PROJECT string from the license server's options file. Optionally, add an LM_PROJECT environment variable to your local machine for local testing using the license server.

### 3. Connect local instance of the simulator

Run the simulator locally by:

```
python main.py
```

The output should say `Registered simulator` followed by--every several seconds--a line saying `Last Event: Idle`.

> NOTE: The next step uses Bonsai CLI commands.
> If you prefer, these opererations can also be performed using your [Bonsai worspace](https://preview.bons.ai/) GUI as described in [Link an unmanaged simulator to Bonsai](https://docs.microsoft.com/en-us/bonsai/guides/run-a-local-sim?tabs=bash%2Ctest-with-ui&pivots=sim-lang-python).

While main.py continues to run, open a new commmand window and use the Bonsai CLI to create a Bonsai brain and start training by:

```
bonsai brain create -n ChangeoverTimes-brain
bonsai brain version update-inkling -f machine_teacher.ink -n ChangeoverTimes-brain
bonsai brain version start-training -n ChangeoverTimes-brain
bonsai simulator unmanaged connect --simulator-name ChangeoverTimes-sim -a Train -b ChangeoverTimes-brain -c Concept
```

The output should say `Simulators Connected: 1`. After a minute or so, you should see lots of activity in the console window that
is running main.py and if you open your [Bonsai worspace](https://preview.bons.ai/) you should see that the brain named ChangeoverTimes-brain
is running training episodes. We'll complete training in a faster way in the next step, so for now you can manually stop training by:

```
bonsai brain version stop-training -n ChangeoverTimes-brain
```

Press Ctrl+C to stop the simulator running main.py in your first console window.

### 4. Build the simulator package and scale training using the cloud

> For this step, you must have Docker installed on your local machine. The community edition of Docker is available for
> [Windows](https://docs.docker.com/docker-for-windows/install), [Linux](https://docs.docker.com/engine/install), and
> [MacOS](https://docs.docker.com/docker-for-mac/install).

Build a Docker container image and push it to your registry.
In the following commands, `<SUBSCRIPTION>` and `<WORKSPACE_ACR_PATH>` should be replaced with
[your workspace details](https://docs.microsoft.com/en-us/bonsai/cookbook/get-workspace-info):

```
docker build -t changeovertimes-container:latest -f Dockerfile ../..
docker tag changeovertimes-container:latest <WORKSPACE_ACR_PATH>/changeovertimes-container:latest
az acr login --subscription <SUBSCRIPTION> --name <WORKSPACE_ACR_PATH>
docker push <WORKSPACE_ACR_PATH>/changeovertimes-container:latest
```

> NOTE: The next step uses Bonsai CLI commands.
> If you prefer, these opererations can also be performed using your [Bonsai worspace](https://preview.bons.ai/) GUI as described
> in [Add a training simulator to your Bonsai workspace](https://docs.microsoft.com/en-us/bonsai/guides/add-simulator?tabs=add-cli%2Ctrain-inkling&pivots=sim-platform-other).

Create a Bonsai simulator package and run training with it by:

```
bonsai simulator package container create -n ChangeoverTimes-pkg -u <WORKSPACE_ACR_PATH>/changeovertimes-container:latest --max-instance-count 25 -r 1 -m 1 -p Linux
bonsai brain version start-training -n ChangeoverTimes-brain --simulator-package-name ChangeoverTimes-pkg
```

Next, open your [Bonsai worspace](https://preview.bons.ai/) and you should see your ChangeoverTimes-brain brain is running training.
If you look in the Train tab, after a few minutes, you will see that simulators have started up and episodes are being executed.
After approximately 200,000 iterations you should see in the training graph shows 100% goal satisfaction and 100% success rate.
You can stop the training at this point or let training continue to run. It will eventually stop when it can no longer find improvements
to reach the goal in a more optimal fashion.
