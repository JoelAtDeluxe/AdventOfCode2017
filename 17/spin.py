

def build_list(base_list, skip, iterations):
  position = 1
  itr = 2
  base_list.append(1)

  for i in range(itr, iterations+1):
    next_pos = (position + skip) % i  # also len(base_list)
    next_pos += 1  # move to next space for writing
    base_list.insert(next_pos, i)
    position = next_pos

  return base_list, position


def mock_build_list(skip, iterations):
  position = 1
  itr = 2
  last_value_at_one = 1

  for i in range(itr, iterations + 1):
    next_pos = (position + skip) % i
    next_pos += 1
    if next_pos == 1:
      last_value_at_one = i
    position = next_pos

  
  return last_value_at_one

def main():
  # skip, steps = 3, 2017
  skip, steps = 343, 2017

  # part 1
  # result, final_insert = build_list([0], skip, steps)
  # print(result[final_insert + 1])

  # Part 2
  steps = 50_000_000
  result = mock_build_list(skip, steps)
  print(result)

if __name__ == "__main__":
    main()