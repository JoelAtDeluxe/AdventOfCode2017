

def main():
    with open('input.txt') as fh:
        content = fh.read()

    currently_reading = None
    group_score = 0
    group_nesting = 0
    advance_char = False

    for idx, char in enumerate(content):
        if advance_char:
            advance_char = False
            continue

        if currently_reading == 'junk':
            if char == '!':
                advance_char = True
            elif char == '>':
                currently_reading = None
        else:
            if char == '{':
                group_nesting += 1
            elif char == '}':
                group_score += group_nesting
                group_nesting -= 1
            elif char == '<':
                currently_reading = 'junk'
            else:  # commas, but these don't seem to matter, given the other rules
                print(f"Found odd character at position: {idx}")
    
    print(f'Total group score: {group_score} group nesting (should be 0): {group_nesting}')


if __name__ == "__main__":
    main()
