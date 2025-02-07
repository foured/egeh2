with open('res/rus_htr.txt', encoding='utf-8') as file:
    words = [w for w in [line.split() for line in file]]
    sorted_words = sorted(words, key=lambda x: x[0].lower())

    with open('res/dbg.txt', 'w', encoding='utf-8') as output_file:
        for pair in sorted_words:
            output_file.write(' '.join(pair) + '\n')

# with open('res/rus_htr.txt', encoding='utf-8') as file:
#     s = file.read()
#     with open('res/dbg.txt', mode='w', encoding='utf-8') as out:
#         out.write(s.lower())

