# Minimize Setup Time

A simple model that chooses the best next item in order to minimize setup time

## Description

This model is very similar to the model presented in the FlexSim documentation:
https://docs.flexsim.com/en/ModelLogic/ReinforcementLearning/Training/.
The concept of the model is the same; a Processor must pull the best Type of item
for the system to perform smoothly.

## Simulation Model Variables

| State | Description |
| ----- | ----- |
| TypesAvailable | An array containing 5 values, indicating which Types are available. |
| LastType | The previous Type of item processed by the Processor. |
| SumSetupTime | The total setup time incurred since the previous action |

| Action | Description | 
| ------ | -------------------- |
| NextType | The next itemtype to process. |

## How to run the sample

### 1. Ensure you can access a Bonsai workspace

If you don't have access to a Bonsai workspace, follow these steps in FlexSim's documentation:
https://docs.flexsim.com/en/ModelLogic/ReinforcementLearning/WorkingWithBonsai/GettingStarted/GettingStarted.html#setup

### 2. Create a new brain with the provided inkling code

In the [Bonsai interface](preview.bons.ai), create a new brain with the code found in the inkling file provided with this example (MinSetupTime.ink).

### 3. Run FlexSim as an unmanaged simulator

1. Open the FlexSim model provided with this sample. 
2. Open the Reinforcement Learning tool, and go to the Bonsai tab.
3. Click the **Register Simulator** button.
4. In the [Bonsai interface](preview.bons.ai), select the new brain, and click the **Train** button. Select the Unmanaged Simulator called **FlexSim Model**.
5. Wait for training to begin, which may take a few minutes. Verify that Bonsai can control the FlexSim model.

Once training has successfully started, click the **Unregister Simulator** button in FlexSim.

If desired, you can follow the FlexSim documentation to [create a managed simulator](https://docs.flexsim.com/en/ModelLogic/ReinforcementLearning/WorkingWithBonsai/GettingStarted/GettingStarted.html#managedsim).