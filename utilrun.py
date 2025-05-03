# with open('res/rus_n10.txt', encoding='utf-8') as file:
#     words = [w for w in [line.split('; ') for line in file]]
#     sorted_words = sorted(words, key=lambda x: x[0].lower())

#     with open('res/dbg.txt', 'w', encoding='utf-8') as output_file:
#         for pair in sorted_words:
#             output_file.write('; '.join(pair))

# with open('res/rus_htr.txt', encoding='utf-8') as file:
#     s = file.read()
#     with open('res/dbg.txt', mode='w', encoding='utf-8') as out:
#         out.write(s.lower())

# with open('res/rus_n10.txt', encoding='utf-8') as file:
#     s = file.read()
#     with open('res/dbg.txt', mode='w', encoding='utf-8') as out:
#         a = s.lower().split(',')
#         for line in a:
#             out.write(line.strip() + '\n')

# with open('res/dbg.txt', encoding='utf-8') as file:
#     with open('res/dbg1.txt', mode='w', encoding='utf-8') as out:
#         for line in file:
#             out.write(line.strip() + ' ' + line)


# with open('res/dbg1.txt', encoding='utf-8') as file:
#     s = file.read().split()
#     print(len(s), len(set(s)))

# with open('res/dbg.txt', encoding='utf-8') as file:
#     with open('res/dbg1.txt', mode='w', encoding='utf-8') as out:
#         for line in file:
#             s = line.lower().strip().replace('е', '...', 1)
#             out.write(s + ' [Е, И]\n')

