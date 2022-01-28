import os
import subprocess
import socket
import json
import numpy as np

from typing import NamedTuple, Dict, Any

import time
from microsoft_bonsai_api.simulator.client import BonsaiClient, BonsaiClientConfig
from microsoft_bonsai_api.simulator.generated.models import SimulatorInterface, SimulatorState, SimulatorSessionResponse

class FlexSimBonsaiEnv():

    def __init__(self, flexsimPath, modelPath, address='localhost', port=5005, verbose=False, visible=False):
        # Perform any global runtime simulator initialization that is needed here.
        self.flexsimPath = flexsimPath
        self.modelPath = modelPath
        self.address = address
        self.port = port
        self.verbose = verbose
        self.visible = visible

        self._launch_flexsim()

    def reset(self, config) -> Dict[str, Any]:
        # Perform initialization in preparation for running an episode using the values in the config dictionary.
        self._set_parameters(config)

        # Reset state from the previous episode that needs to be cleared.
        self._reset_flexsim()
        state, reward, done = self._get_observation()

        observation = {
            # If 'sim_halted' is set to True, that indicates that the simulator is unable to continue and the
            # episode will be discarded. If your simulator cannot reach an unrecoverable state, always set 'sim_halted'
            # to False.
            'sim_halted': False,
            #'key': value,
        }
        # Add simulator state as dictionary with key as the state and value as the state's value.
        for key, value in state.items():
            observation[key] = value
        return observation

    def step(self, action) -> Dict[str, Any]:
        # Perform a simulation step using the values in the action dictionary.
        self._set_parameters(action)
        
        self._take_action()
        state, reward, done = self._get_observation()

        observation = {
            'sim_halted': False,
            #'key': value,
        }
        # Add simulator state as dictionary with key as the state and value as the state's value.
        for key, value in state.items():
            observation[key] = value
        return observation

    def close(self):
        self._close_flexsim()
        
    def seed(self, seed=None):
        self.seedNum = seed
        return self.seedNum

    
    def _launch_flexsim(self):
        if self.verbose:
            print("Launching " + self.flexsimPath + " " + self.modelPath)

        args = [self.flexsimPath, self.modelPath, "-training", self.address + ':' + str(self.port)]
        if self.visible == False:
            args.append("-maintenance")
            args.append("nogui")
        self.flexsimProcess = subprocess.Popen(args)

        self._socket_init(self.address, self.port)
    
    def _close_flexsim(self):
        self.flexsimProcess.kill()

    def _release_flexsim(self):
        if self.verbose:
            print("Sending StopWaiting message")
        self._socket_send(b"StopWaiting?")

    def _reset_flexsim(self):
        if self.verbose:
            print("Sending Reset message")
        resetString = "Reset?"
        if hasattr(self, "seedNum"):
            resetString = "Reset:" + str(self.seedNum) + "?"
        self._socket_send(resetString.encode())

    def _get_observation(self):
        if self.verbose:
            print("Waiting for Observation message")
        observationBytes = self._socket_recv()
        self.lastObservation = observationBytes.decode('utf-8')
        state, reward, done = self._convert_to_observation(observationBytes)

        return state, reward, done
    
    def _take_action(self):
        if self.verbose:
            print("Sending Action message")
        actionMessage = "TakeAction?"
        self._socket_send(actionMessage.encode())

    def _get_parameter(self, name):
        if self.verbose:
            print("Sending GetParam " + name + " message")
        getParamString = "GetParam:" + name + "?"
        self._socket_send(getParamString.encode())

        if self.verbose:
            print("Waiting for GetParam:" + name + " message")
        getParamBytes = self._socket_recv()

        return json.loads(getParamBytes)

    def _set_parameter(self, name, value):
        if self.verbose:
            print("Sending SetParam message")
        getParamString = "SetParam:" + name + ":" + str(value) + "?"
        self._socket_send(getParamString.encode())

    def _set_parameters(self, params):
        if self.verbose:
            print("Sending SetParams message")
        getParamString = "SetParams:" + json.dumps(params, cls=NumpyEncoder) + "?"
        self._socket_send(getParamString.encode())


    def _socket_init(self, host, port):
        if self.verbose:
            print("Waiting for FlexSim to connect to socket on " + self.address + ":" + str(self.port))

        self.serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.serversocket.bind((host, port))
        self.serversocket.listen()

        (self.clientsocket, self.socketaddress) = self.serversocket.accept()
        if self.verbose:
            print("Socket connected")
        
        if self.verbose:
            print("Waiting for READY message")
        message = self._socket_recv()
        if self.verbose:
            print(message.decode('utf-8'))
        if message != b"READY":
            raise RuntimeError("Did not receive READY! message")

    def _socket_send(self, msg):
        totalsent = 0
        while totalsent < len(msg):
            sent = self.clientsocket.send(msg[totalsent:])
            if sent == 0:
                raise RuntimeError("Socket connection broken")
            totalsent = totalsent + sent

    def _socket_recv(self):
        chunks = []
        while 1:
            chunk = self.clientsocket.recv(2048)
            if chunk == b'':
                raise RuntimeError("Socket connection broken")
            if chunk[-1] == ord('!'):
                chunks.append(chunk[:-1])
                break;
            else:
                chunks.append(chunk)
        return b''.join(chunks)
        

    def _convert_to_observation(self, spaceBytes):
        observation = json.loads(spaceBytes)
        state = observation["state"]
        if isinstance(state, list):
            state = np.array(observation["state"])
        reward = observation["reward"]
        done = (observation["done"] == 1)
        return state, reward, done


class NumpyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        return json.JSONEncoder.default(self, obj)


def main():
    print(f"Starting FlexSim Bonsai Environment Registration Script")

    workspace = os.getenv("SIM_WORKSPACE")
    accesskey = os.getenv("SIM_ACCESS_KEY")

    config_client = BonsaiClientConfig()
    client = BonsaiClient(config_client)

    registration_info = SimulatorInterface(
        name="FlexSim22.1",
        timeout=60,
        simulator_context=config_client.simulator_context,
        description=None,
    )

    registered_session: SimulatorSessionResponse = client.session.create(workspace_name=config_client.workspace, body=registration_info)
    print(f"Registered simulator. {registered_session.session_id}")

    sequence_id = 1
    sim_model = FlexSimBonsaiEnv(
        flexsimPath = "C:/Program Files/FlexSim 2022 Update 1 Beta/program/flexsim.exe",
        modelPath = "C:/Users/USERNAME/Documents/FlexSim 2022 Projects/MyModel.fsm",
        verbose = True,
        visible = True
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

            if event.type == "Idle":
                time.sleep(event.idle.callback_time)
            elif event.type == "EpisodeStart":
                sim_model_state = sim_model.reset(event.episode_start.config)
            elif event.type == "EpisodeStep":
                sim_model_state = sim_model.step(event.episode_step.action)
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