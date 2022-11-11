# Job Scheduling

## Model Description
The model is inspired by a sheet-metal production line. Items arrive at the beginning of the line
in batches of 10. Each item moves through the entire line. Only one item can be processed at a time
on each machine. So at most, there can only be four items in progress at any given time. A machine 
cannot accept a new item until the current item is accepted by the downstream machine.

The time required at each machine varies from item to item. Because of this, processing sequence
is central to system performance. A good sequence minimizes the time a machine spends waiting
for a downstream machine.

### Model Visualization
The color of each item represents how long it has been blocked by a downstream item. Items begin
as light gray. When an item is blocked, it fades more and more towards red. Once an item is 
finished, its color is an indicator of the total time is was blocked during processing.

After all ten items in the batch have been completed, the model creates a new item that
represents the batch as a whole. The batch item's color is the average color of all the
items in the batch. In addition, the batch item is placed in one of three queues, depending
on whether the average block time was high, acceptable, or low.

By running the model for a long time, you can see the effectiveness of the algorithm that
sequences items.

## Brain Description

The Bonsai brain is designed to choose which item to process given the set of remaining
items in the batch. This decision happens whenever the first machine in the line
becomes available and there is more than one item remaining in the batch.

### Observations (SimState)

* **JobTimes** is a table with 10 rows and four columns. The value at row *i*, column *j* 
  indicates the time required by item *i* on machine *j*. The set of items shown in
  the table are the items that have not started processing yet. Any extra rows show
  zero for the time required for that item.
  
  This observation allows Bonsai to see what jobs are available and how long they
  will take at each machine.

* **WIPTimes** is an array with 6 values. These values are the times required by each
  of the three items in progress for their remaining steps. If less than three
  items are present, trailing values are set to zero.

  This observation allows Bonsai to see what's currently in progress.

* **BlockTime** is a single number. It records the total block time for all items
  since the previous observation. This value increases as items are blocked by other
  items in the line.

  This observation allows Bonsai to understand its effectiveness. The brain's goal is
  to minimize this value.

* **NextJobMask** is an array of values. It communicates which actions are valid. For
  example, if there are only 6 items left in the batch, then it would be invalid to
  attempt to choose items 7, 8, 9, or 10.

  > NextJobMask prohibits Bonsai from taking invalid actions, but is not included
  in the learning state.

### Actions

* **NextJob** represents the choice that Bonsai can make. The options for that choice
  start with *J1* and end with *J10*. If Bonsai chooses J2, that indicates that the
  second item of the remaining items should begin processing next.

### Using an Action Mask Concept

This brain contains two concepts. The first concept is called RemoveMask. Its purpose
is to reduce the input state by removing the NextJobMask observation. In order to
train the brain, you'll need to build this concept. Once the concept is built, you
can train.

### Goal

The goal of the brain is to minimize the BlockTime observation.

## Training Notes

Most of the training happens within the first million iterations.