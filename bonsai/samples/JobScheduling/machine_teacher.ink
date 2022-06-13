inkling "2.0"
using Goal

# The number of jobs per batch
const JobCount = 10

# The number of machines each job goes through
const StepCount = 4

# This type represents the observations used for learning
# that come from the FlexSim model.
type LearningState {
    # The table of times for jobs that still have not begun.
    JobTimes: number<0 .. 60>[StepCount][JobCount],

    # The step times for the incomplete steps of the jobs in progress.
    WIPTimes: number<0 .. 60>[(StepCount - 1) * StepCount / 2],

    # The total time any processor has been blocked, since the last action
    # A processor is blocked from the time it finishes the current job
    # until the next processor can accept the job.
    BlockTime: number,
}

# SimState represents all observations from the FlexSim model.
# Only the values contained in LearningState are used for learning.
type SimState extends LearningState {
    # NextJobMask is an array that tells Bonsai which jobs it can start
    NextJobMask: number<0, 1, >[JobCount],

    # DrawData contains values used to generate a visualization during training
    DrawData: number[JobCount + 3],
}

# SimAction represents the actions Bonsai can take.
# In this example, there is only one action - choose one of 10
# jobs to start.
type SimAction {
    NextJob: number<J1 = 1, J2 = 2, J3 = 3, J4 = 4, J5 = 5, J6 = 6, J7 = 7, J8 = 8, J9 = 9, J10 = 10, >,
}

simulator FlexSimSimulator(action: SimAction): SimState {

}

function ApplyJobMask(s: SimState) {
    return constraint SimAction {
        NextJob: number<mask s.NextJobMask>
    }
}

graph (input: SimState) {

    # The RemoveMask concept removes the data it doesn't need for learning.
    concept RemoveMask(input): LearningState {
        programmed function (s: SimState): LearningState {
            return LearningState(s)
        }
    }

    # The MinimizeBlockTime concept learns to choose a good job to start, based on the actions
    # "Good" is defined as choosing a jobs so that the block time is minimized.
    output concept MinimizeBlockTime(RemoveMask): SimAction {
        curriculum {

            source FlexSimSimulator
            mask ApplyJobMask

            training {
                EpisodeIterationLimit: 800,
                NoProgressIterationLimit: 1000000,
            }

            goal (State: SimState) {
                minimize BlockTime:
                    State.BlockTime
                    in Goal.RangeBelow(0)
            }
        }
    }
}
