# Advent of Code 2017 solutions

(Started in Dec 2018)

## Notes on some of the puzzles

### Day 17

So, the part one of this problem is pretty straight forward. There's an obvious time saving where you don't do each index change in the list, and instead just calculate the next position.

Part 2 expands on this by making a huge number of updates to the array. But, a couple of notes:

1. Because of the way the logic works, the 0th index is always 0 (so, we don't need to search the array to find 0)
2. Since we always only need the first index, we just to figure out when we put something new into that spot, so we don't even have to update the array

