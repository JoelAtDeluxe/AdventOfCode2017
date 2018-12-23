

def load_file(path):
    lines = []
    with open(path, 'r') as fh:
        for line in fh:
            lines.append(line.strip())
    return lines


if __name__ == '__main__':
    passphrases = load_file('passwords.txt')

    def has_no_repeat_words(words):
        return len(words) == len(set(words))

    def has_no_anagrams(words):
        sorted_words = [''.join(sorted(word)) for word in words]
        return len(sorted_words) == len(set(sorted_words))

    intermediate = map(lambda x: x.split(), passphrases)
    # intermediate = filter(has_no_repeat_words, intermediate)  # agagram work does the same thing
    intermediate = filter(has_no_anagrams, intermediate) 
    valid_passwords = list(intermediate)
    
    # P1 solution
    # for phrase in passphrases:
    #     words = phrase.split()
    #     if len(words) == len(set(words)):
    #         valid_count = valid_count + 1

    print(f"There are {len(valid_passwords)} valid passwords")
