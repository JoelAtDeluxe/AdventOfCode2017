

def load_file(path):
    lines = []
    with open(path, 'r') as fh:
        for line in fh:
            lines.append(line.strip())
    return lines


if __name__ == '__main__':
    passphrases = load_file('passwords.txt')

    valid_count = 0
    for phrase in passphrases:
        words = phrase.split()
        if len(words) == len(set(words)):
            valid_count = valid_count + 1

    print(f"There are {valid_count} valid passwords")
