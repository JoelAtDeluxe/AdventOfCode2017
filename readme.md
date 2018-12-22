# Advent of Code 2017 solutions

(Started in Dec 2018)

## Notes

### 1

### 2

### 3

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
   * if `x > E && x < N` => Quadrant 1 (NE)
   * If `x > N && x < W` => Quadrant 2 (NW)
   * if `x > W && x < S` => Quadrant 3 (SW)
   * If `x > W && x > E` => Quadrant 4 (SE)
   * If `x` is equal to `N, S, E, W` then already on the axis. steps remaining = n 
   * (Anything else must be an error)
4. If you are in a quadrant, move towards the closest axis.
   * Quad 1 => min(x - E, N - x) [this will be the number of steps we need to take to reach the axis]
   * Quad 2 => min(x - N, W - x)
   * Quad 3 => min(x - W, S - x)
   * Quad 4 => min(x - S, E - x) # This one is flawed. Choose the lowest number that's greater than 0
   * 