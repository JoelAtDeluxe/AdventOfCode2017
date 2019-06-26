import re
from particle import Particle, ParticleWithName


def parse_particle(s):
    pattern = r'[pva]=<([^>]+)>'
    itr = re.finditer(pattern, s)
    # breakpoint()
    p = [int(f) for f in next(itr).group(1).split(',')]
    v = [int(f) for f in next(itr).group(1).split(',')]
    a = [int(f) for f in next(itr).group(1).split(',')]
    return Particle(p, v, a)


def parse_input(path):
    particles = []
    with open(path, 'r') as fh:
        for line in fh:
            particles.append(parse_particle(line.strip()))

    return particles


def closest_particle_long_term(particles):
    def min_fun(i):
        return particles[i].dist_from_origin()

    # while not all([p.is_repelling() for p in particles]):
    for _ in range(1000):
        print(min(range(len(particles)), key=min_fun))
        for p in particles:
            p.tick()
        # breakpoint()
    
    index_min = min(range(len(particles)), key=min_fun)
    return index_min


def closest_particle_long_term_with_collision_culling(particles):
    unculled = [ParticleWithName(i, v) for i, v in enumerate(particles)]

    for _ in range(1000):
        for p in unculled:
            p.tick()
        collisons = {}
        for p in unculled:
            vals = collisons.get(p.get_position_tuple(), [])
            vals.append(p.name)
            collisons[p.get_position_tuple()] = vals
        
        collisons = [v for k, v in collisons.items() if len(v) > 1]
        if len(collisons) > 0:  # do the culling
            flatted_indexes = [v for lst in collisons for v in lst]
            unculled = [v for v in unculled if v.name not in flatted_indexes]
        
    min_item = min(unculled, key=lambda x: x.dist_from_origin())
    return min_item.name

def main():
    particles = parse_input('input.txt')

    # part 1
    result = closest_particle_long_term(particles)
    print(result)

    # part 2
    # result = closest_particle_long_term_with_collision_culling(particles)
    # print(result)

if __name__ == "__main__":
    main()
