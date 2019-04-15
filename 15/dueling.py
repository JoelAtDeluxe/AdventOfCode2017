

def make_gen(initial, factor, n_factor):
  divisible = (2 ** n_factor) - 1
  def gen():
    rtn = initial
    while True:
      rtn = (rtn * factor) % 2147483647
      if (rtn & divisible) == 0:
        yield rtn
  return gen()


def main():
  # Part 1
  # a = make_gen(703, 16807, 0)
  # b = make_gen(516, 48271, 0)
  # num_rounds = 40_000_000

  # Part 2
  a = make_gen(703, 16807, 2)
  b = make_gen(516, 48271, 3)
  num_rounds = 5_000_000

  num_matches = calc_num_matches(a, b, 16, num_rounds)
  print(f"Got {num_matches} matches in {num_rounds} rounds")


def calc_num_matches(gen_a, gen_b, num_bit_match, rounds):
  match_count = 0
  mod = 2**num_bit_match
  for _ in range(rounds):
    if _ % 1000 == 0:
      print(f"At round: {_}", end='\r')

    a_val = next(gen_a)
    b_val = next(gen_b)
    if (a_val % mod) == (b_val % mod):
      match_count += 1

  return match_count

if __name__ == "__main__":
    main()