#!/usr/bin/env python3

import os
import time
import sys
import random
from microsoft_bonsai_api.simulator.client import BonsaiClient, BonsaiClientConfig
from microsoft_bonsai_api.simulator.generated.models import SimulatorInterface, SimulatorState, SimulatorSessionResponse

# Add parent directory containing the connector folder to path.
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from connector.flexsim_bonsai_env import FlexSimBonsaiEnv

def main():
    """
    Creates a Bonsai simulator session and executes Bonsai episodes.
    """

    workspace = os.getenv("SIM_WORKSPACE")
    accesskey = os.getenv("SIM_ACCESS_KEY")

    config_client = BonsaiClientConfig()
    client = BonsaiClient(config_client)

    registration_info = SimulatorInterface(
        name="ChangeoverTimes-sim",
        timeout=60,
        simulator_context=config_client.simulator_context,
        description=None,
    )

    print(f"config: {config_client.server}, {config_client.workspace}")
    registered_session: SimulatorSessionResponse = client.session.create(workspace_name=config_client.workspace, body=registration_info)
    print(f"Registered simulator. {registered_session.session_id}")

    sequence_id = 1
    sim_model = FlexSimBonsaiEnv(
        flexsimPath = "C:/FlexSim/program/flexsim.exe",
        modelPath = "C:/src/samples/ChangeoverTimes/Model.fsm",
        verbose = True,
        visible = False
        )
    print(f"FlexSim Environment Ready")
    sim_model_state = { 'sim_halted': False }

    try:
        while True:
            sim_state = SimulatorState(sequence_id=sequence_id, state=sim_model_state, halted=sim_model_state.get('sim_halted', False))
            event = client.session.advance(
                workspace_name=config_client.workspace,
                session_id=registered_session.session_id,
                body=sim_state,
            )
            sequence_id = event.sequence_id
            print(f'[{time.strftime("%H:%M:%S")}] Last Event: {event.type}')

            if event.type == "Idle":
                time.sleep(event.idle.callback_time)
            elif event.type == "EpisodeStart":
                print(f"config {event.episode_start.config}")
                seed = random.randint(1, 255)
                sim_model.seed(seed)
                sim_model_state = sim_model.reset(event.episode_start.config)
                print(f"state {sim_model_state}")
            elif event.type == "EpisodeStep":
                print(f"action {event.episode_step.action}")
                sim_model_state = sim_model.step(event.episode_step.action)
                print(f"state {sim_model_state}")
            elif event.type == "EpisodeFinish":
                sim_model_state = { 'sim_halted': False }
            elif event.type == "Unregister":
                print(f"Simulator Session unregistered by platform because '{event.unregister.details}'")
                return
    except BaseException as err:
        client.session.delete(workspace_name=config_client.workspace, session_id=registered_session.session_id)
        print(f"Unregistered simulator because {type(err).__name__}: {err}")

if __name__ == "__main__":
    main()
