

def main():
    with open('input.txt') as fh:
        content = fh.read()

    currently_reading_junk = False
    group_score = 0
    group_nesting = 0
    advance_char = False
    removed_char_count = 0
    last_junk_index = 0

    for idx, char in enumerate(content):
        if advance_char:
            advance_char = False
            continue

        if currently_reading_junk:
            if char == '!':
                removed_char_count -= 2  # exclude this character and next
                advance_char = True
            elif char == '>':
                currently_reading_junk = False
                removed_char_count += idx - last_junk_index - 1  # -1 to remove the "<" that is counted as part of the range
        else:
            if char == '{':
                group_nesting += 1
            elif char == '}':
                group_score += group_nesting
                group_nesting -= 1
            elif char == '<':
                currently_reading_junk = True
                last_junk_index = idx
            
    print(f'Total group score: {group_score} group nesting (should be 0): {group_nesting}')
    print(f'Removed non-cancelled garbage characters: {removed_char_count}')


if __name__ == "__main__":
    main()
