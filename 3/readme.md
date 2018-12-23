# Question 3

## Part 1

For p1, the grid could be divided up into quadrants, split by an x or y axis.
If this is done, we can figure out how far the the element is from one of the nearest axis,
and then walk the axis back to the center (which by definition will be 1)

From their example:

```
                              ^
                              | +y (AKA _N_orth)
                              |
                      17  16  15  14  13
                      18   5   4   3  12
- x (AKA _W_est) <--- 19   6   1   2  11  ---> + x (AKA _E_ast)
                      20   7   8   9  10
                      21  22  23  24  25
                              |
                              | -y (AKA _S_outh)
```

Note that it does not matter which axis we choose. As long as we walk towards one and never overshoot the axis, it
will always produce the shortest route.

* + x axis values can be derived by the following recursive algorithm:
  ```python
    def value(steps_away):
      if steps_away == 0:
        return 1
      # sequence = 2, 11, 28, 53, 
      return value(steps_away - 1) + (8 * steps_away) - 7
  ```
* - x axis values can be dervied from the following:
  ```python
    def value(steps_away):
      if steps_away == 0:
        return 1
      # sequence = 6, 19, 40, 69
      return value(steps_away - 1) + (8 * steps_away) - 3
  ```
* + y axis:
  ```python
    def value(steps_away):
      if steps_away == 0:
        return 1
      # sequence = 6, 19, 40, 69
      return value(steps_away - 1) + (8 * steps_away) - 5
  ```
* - y axis:
  ```python
    def value(steps_away):
      if steps_away == 0:
        return 1
      # sequence = 6, 19, 40, 69
      return value(steps_away - 1) + (8 * steps_away) - 1
  ```

Determinining quandrant approach:
let n = the starting number

1. Determine square bounding box
   1. sqrt number. find the next whole odd number (if sqrt(n) is whole and odd, then use this instead)
   2. Note: We will always be on the outer edge of the grid with this approach.
2. Calculate N, E, S, W axis values. Will only need to calculate each axis for x, where x = grid_length/2 (rounded down)
3. Do some checks:
   * if `x <  E` => Quadrant 4 (SE) -> steps to axis = (E - val) [We are moving towards East]
   * If `x <= N` => Quadrant 1 (NE) -> Steps to axis = min(N - val, val - E) [Moving towards closest axis]
   * If `x <= W` => Quadrant 2 (NW) -> Steps to axis = min(W - val, val - N) [Moving towards closest axis]
   * If `x <= S` => Quadrant 3 (SW) -> Steps to axis = min(S - val, val - W) [Moving towards closest axis]
   * Else (`x > S`) Quadrant 4 (SE) -> steps to axis = val - S
   * Then `x` is equal to `N, S, E, W`. steps remaining = n 
   * (Anything else must be an error)

## Part 2

I guess I can't avoid building out the grid now.

We can again think of the grid in only odd-lengthed, square dimensions, and simply grow the grid as necesary while building it out. If we do this, then we need to make the following considerations:

1. We need to center the old grid in the new grid. Using the array expansion helps a lot here.
2. When the grid grows, we need to remember to adjust our indices into the grid. Since we grow by 2 every time (to maintain an odd dimension), we need to increment both indicies by 1
3. We only need to grow the grid when the current section is too small. This will always happen at `x[n-1][n-1]`, or when we've counted up `n*n` cells. I chose to do this via the latter, but the former is probably a better solution.

Navigating the grid is somewhat odd. If you trace it out, what you basically do is take a certain number of steps, then turn, then take the same number of steps, then turn, then repeat this process with 1 more step than the last time. Written out, you do this:
1 step forward, turn, 1 step forward, turn, 2 steps forward, turn, 2 steps forward, turn, ...

I chose to use generators to help me with both maintaining the "direction" to move in, as well as what cell number to stop on. The former simply hides some book keeping, while the latter makes acting on each step much more approachable. 
