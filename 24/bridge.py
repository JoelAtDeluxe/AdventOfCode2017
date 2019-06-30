from piece import Piece


def parse_input(path):
    components = []
    with open(path, 'r') as fh:
        for line in fh:
            components.append(line.strip())
    return components


def sort_pieces(pieces):
    all_pieces = []
    for piece in pieces:
        n, s = [int(v) for v in piece.split('/')]
        all_pieces.append(Piece(n, s))

    pieces_by_side = {}

    for p in all_pieces:
        for face in (p.north, p.south):
            for ap in all_pieces:
                if ap.can_fit_side(face):
                    matching_pieces = pieces_by_side.get(face, set())
                    matching_pieces.add(ap)
                    pieces_by_side[face] = matching_pieces

    # turning back into a list to preserve ordering
    pieces_by_side = {k: list(v) for k, v in pieces_by_side.items()}
    return pieces_by_side


def clone_bridge(bridge):
    return [p.clone() for p in bridge]


def segments_for_side(pieces, side):
    if side == -1:
        return []

    segments = pieces[side]
    rtn = []
    for s in segments:
        if s.can_fit_side(side):
            rtn.append(s)
    return rtn


def try_bridges(bridge, next_side, pieces, all_bridges):
    """ This is a very lightly optimized brute force technique """
    next_pieces = segments_for_side(pieces, next_side)
    
    for piece in next_pieces:
        # Add to the bridge
        bridge.append(piece)
        piece.fit_with(next_side)

        # check bridge's exposed end
        new_bridge_end = piece.get_other_side(next_side)

        # Look for more pieces
        try_bridges(bridge, new_bridge_end, pieces, all_bridges)

        # Done with the piece we just used, so return it to the bin
        piece = bridge.pop()
        piece.reset()
    else:  # No more pieces, so this is a complete bridge
        # breakpoint()
        all_bridges.append(clone_bridge(bridge))
    return


def print_bridge(bridge):
    return '--'.join([repr(p) for p in bridge])


def sum_bridge(bridge):
    return sum([p.size for p in bridge])


def find_longest_bridges(all_bridges):
    longest_bridges = []
    bridge_length = 0
    for b in all_bridges:
        if len(b) > bridge_length:
            longest_bridges = [b]
            bridge_length = len(b)
        elif len(b) == bridge_length:
            longest_bridges.append(b)
    return longest_bridges


def main():
    parts = parse_input('input.txt')
    # parts = parse_input('input_sample.txt')
    by_size = sort_pieces(parts)

    all_bridges = []
    
    try_bridges([], 0, by_size, all_bridges)
    
    # Part 1
    best_bridge = max(all_bridges, key=sum_bridge)
    print(f"Best bridge to use is: \n\t{best_bridge} \nwith a weight of: \n\t{sum_bridge(best_bridge)}")

    # Part 2
    lb = find_longest_bridges(all_bridges)
    best_remaining_bridge = max(lb, key=sum_bridge)
    print(f"Best, longest bridge is: \n\t{best_remaining_bridge} \nwith a weight of: \n\t{sum_bridge(best_remaining_bridge)}")
    

if __name__ == "__main__":
    main()
