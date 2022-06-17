inkling "2.0"

using Math
using Goal

# State received from the simulator after each iteration
type ObservableState {
    LastItemType: number,
    Time: number,
    Throughput: number,
}

# Action provided as output by policy and sent as input to the simulator
type SimAction {
    ItemType: number<1 .. 5 step 1>
}

# Per-episode configuration that can be sent to the simulator.
# All iterations within an episode will use the same configuration.
type SimConfig {
    LastItemType: number,
}

simulator FlexSimSimulator(action: SimAction, config: SimConfig): ObservableState {
}

# Define a concept graph
graph (input: ObservableState) {
    concept MinimizeChangeovers(input): SimAction {
        curriculum {
            # The source of training for this concept is a simulator
            # that takes an action as an input and outputs a state.
            source FlexSimSimulator

            # Add goals here describing what you want to teach the brain
            # See the Inkling documentation for goals syntax
            # https://docs.microsoft.com/bonsai/inkling/keywords/goal
            goal (State: ObservableState) {
                maximize `Throughput`:
                    State.Throughput
                    in Goal.RangeAbove(0)
                reach `Time`:
                    State.Time
                    in Goal.RangeAbove(1000)
            }

            training {
              EpisodeIterationLimit: 250
            }

            lesson `Initial Conditions` {
                # Specify the configuration parameters that should be varied
                # from one episode to the next during this lesson.
                scenario {
                    LastItemType: number<1 .. 5 step 1>,
                }
            }
        }
    }
}
