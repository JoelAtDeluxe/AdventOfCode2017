import math


def build_axis_values_function(offset):
    def build_it(steps):
        rtn = [1]
        for i in range(steps):
            rtn.append( rtn[i] + 8*(i+1) - offset )

        return rtn[1:]
    return build_it


def navigate(start):
    
    if start == 1: # a quick out here, since 1 is a known path, and causes problems below
        return 0

    # determine the bounding box for this memory section (i.e. get n for the n x n box we generate)
    root = math.sqrt(start)
    if root != int(root):
        root = int(root) + 1
        if root % 2 == 0:
            root += 1
    
    # Get the minimum number of steps to walk to the center from the outer edge
    steps = int(root//2)

    # Generate axis values
    north_axis = build_axis_values_function(5)(steps)
    south_axis = build_axis_values_function(1)(steps)
    east_axis = build_axis_values_function(7)(steps)
    west_axis = build_axis_values_function(3)(steps)

    walking_steps = 0
    if start < east_axis[-1]:
        walking_steps = east_axis[-1] - start
    elif start < north_axis[-1]:
        walking_steps = min(north_axis[-1] - start, start - east_axis[-1])
    elif start < west_axis[-1]:
        walking_steps = min(west_axis[-1] - start, start - north_axis[-1])
    elif start < south_axis[-1]:
        walking_steps = min(south_axis[-1] - start, start - west_axis[-1])
    else:
        walking_steps = start - south_axis[-1]
    
    walking_steps += steps

    return walking_steps

print(f'{1} => {navigate(1)}')
print(f'{2} => {navigate(2)}')
print(f'{3} => {navigate(3)}')
print(f'{4} => {navigate(4)}')
print(f'{5} => {navigate(5)}')
print(f'{6} => {navigate(6)}')
print(f'{7} => {navigate(7)}')
print(f'{8} => {navigate(8)}')
print(f'{9} => {navigate(9)}')
print(f'{12} => {navigate(12)}')
print(f'{23} => {navigate(23)}')
print(f'{1024} => {navigate(1024)}')
print(f'{265149} => {navigate(265149)}')
