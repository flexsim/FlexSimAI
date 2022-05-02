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
type LearningState {
    # the current model time
    Time: number,

    # the number of jobs remaining in the batch
    JobsRemaining: number<0 .. JobCount step 1>,

    # The table of times for jobs that still have not begun.
    # Note the order of dimensions
    JobTimes: number<0 .. 60>[StepCount][JobCount],

    # The step times for the incomplete steps of the jobs in progress.
    WIPTimes: number<0 .. 60>[(StepCount - 1) * StepCount / 2],

    # The total time any processor has been blocked, since the last action
    # A processor is blocked from the time it finishes the current job
    # until the next processor can accept the job.
    BlockTime: number,

    # The total number of items finished, since the last action
    Throughput: number,
}

# I also include the next job mask
# These values are ignored for learning
type SimState extends LearningState {
    NextJobMask: number<0,1,>[20],
}

type SimAction {
    NextJob: number<
        J1 = 1, 
        J2 = 2,
        J3 = 3,
        J4 = 4,
        J5 = 5,
        J6 = 6,
        J7 = 7,
        J8 = 8,
        J9 = 9,
        J10 = 10,
        J11 = 11,
        J12 = 12,
        J13 = 13,
        J14 = 14,
        J15 = 15,
        J16 = 16,
        J17 = 17,
        J18 = 18,
        J19 = 19,
        J20 = 20,
    >,
}

type SimConfig {
    JobCount: number<5..20 step 1>,
    StepCount: number<2..4 step 1>,
}

function ApplyJobMask(s: SimState) {
    return constraint SimAction { NextJob: number<mask s.NextJobMask> }
}

# Using the flexsim simulator
simulator FlexSimSimulator(action: SimAction, config: SimConfig): SimState {
    
}

graph (input: SimState) {

    concept RemoveMask(input) : LearningState {
        programmed function(s: SimState): LearningState {
            # use cast to avoid writing out all the fields one by one -- works if LearningState is a subset of ObservableState
            return LearningState(s)
        }
    }

    output concept MinimizeBlockTime(RemoveMask) : SimAction {
        curriculum {
            # The source of training for this concept is a simulator
            # that takes an action as an input and outputs a state.
            source FlexSimSimulator

            training {
                EpisodeIterationLimit: 250
            }

            mask ApplyJobMask

            # One way to express the goal is to minimize block time.
            # The simulation should also run for about 1000 time units.
            goal (State: SimState) {
                minimize BlockTime:
                    State.BlockTime
                    in Goal.RangeBelow(100)
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