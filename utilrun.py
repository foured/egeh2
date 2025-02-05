with open('res/rus_n4_2025.txt', encoding='utf-8') as file:
    words = [w for w in [line.split() for line in file]]
    sorted_words = sorted(words, key=lambda x: x[0].lower())

    with open('res/sorted_rus_n4_1_2025.txt', 'w', encoding='utf-8') as output_file:
        for pair in sorted_words:
            output_file.write(' '.join(pair) + '\n')