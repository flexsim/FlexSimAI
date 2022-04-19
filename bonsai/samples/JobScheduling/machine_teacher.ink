# This is the file for the scheduling example
# In this example, there are StepCount stations in sequence.
# The model supports up to 4 stations.
# There is a list of jobs. Each job knows the time it will
# take at each step. The job of the brain is to choose
# which job to do next. That job is best expressed as an index.

inkling "2.0"
using Goal
using Math

# The number of jobs per batch
const JobCount = 5

# The number of steps that each job goes through
const StepCount = 2

# This type represents the observations that come from FlexSim,
# in this particular model.
type SimState {
    # the current model time
    Time: number,

    # the number of jobs remaining in the batch
    JobsRemaining: number<0 .. JobCount step 1>,

    # The table of times for jobs that still have not begun.
    # Note the order of dimensions
    JobTimes: number<0 .. 60>[StepCount][JobCount],

    # The step times for the incomplete steps of the jobs in progress.
    WIPTimes: number<0 .. 60>[(StepCount - 1) * StepCount / 2],

    # The total time any processor has been blocked.
    # A processor is blocked from the time it finishes the current job
    # until the next processor can accept the job.
    TotalBlockTime: number,
}

type SimAction {
    NextJob: number<1 .. JobCount step 1>,
}

type SimConfig {
    JobCount: number<5..20>,
    StepCount: number<2..4>,
}

# Using the flexsim simulator
simulator FlexSimSimulator(action: SimAction, config: SimConfig): SimState {
    
}

graph (input: SimState) {
    concept MinimizeBlockTime(input): SimAction {
        curriculum {
            # The source of training for this concept is a simulator
            # that takes an action as an input and outputs a state.
            source FlexSimSimulator

            training {
                EpisodeIterationLimit: 250
            }

            # One way to express the goal is to minimize block time.
            # The simulation should also run for about 1000 time units.
            goal (State: SimState) {
                minimize BlockTime:
                    State.TotalBlockTime
                    in Goal.Range(0, 100)
                reach Time:
                    State.Time
                    in Goal.RangeAbove(1000)
            }

            # It's not really a lesson; I just want bonsai to tell the model
            # how it should be configured
            lesson `Current lesson` {
                scenario {
                    JobCount: JobCount,
                    StepCount: StepCount,
                }
            }
        }
    }
}

