inkling "2.0"
using Goal

# Define the observation space
type SimState {
    # TypesAvailable contains one value for each type; 1 if that type is present, 0 if it isn't
    TypesAvailable: number[5],

    # LastType is set to the type last done by the processor.
    # It is enumerated because Type is a category value.
    LastType: number<Type1 = 1, Type2 = 2, Type3 = 3, Type4 = 4, Type5 = 5, NoType = 6>,

    # SumSetupTime is set to the total setup time since the previous action
    SumSetupTime: number,
}

# Define the action space
type SimAction {
    # NextType indicates which type should be processed next
    NextType: number<Type1 = 1, Type2 = 2, Type3 = 3, Type4 = 4, Type5 = 5>,
}

simulator Simulator(action: SimAction): SimState {
}

# Define a concept graph
graph (input: SimState): SimAction {
    concept Concept1(input): SimAction {
        curriculum {
            # The source of training for this concept is a simulator
            # that takes an action as an input and outputs a state.
            source Simulator

            training {
                EpisodeIterationLimit: 100,
                NoProgressIterationLimit: 100000,
            }

            # The goal is to get the setup time down to zero, or as close as possible
            goal (State: SimState) {
                minimize SetupTime:
                    State.SumSetupTime
                    in Goal.RangeBelow(0)
            }
        }
    }
}
