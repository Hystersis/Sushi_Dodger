from itertools import count, repeat

def func(chr_num):
    w = 4 + chr_num * 7 + (chr_num - 1)
    # This calculates the width according to the construct
    Xw = max((chr_num * 7 + (chr_num - 1) - 5) // 2, 0)
    # Exclusive w, all width is based off 8bit font at 16 pt
    Lw = (chr_num * 7 + (chr_num - 1))
    instructions = {(0, 0): (0, 0, 2, 9), (w - 2, 0): (7, 0, 2, 9)}
    instructions = instructions | {k: v for k, v in zip(zip(count(4), repeat(1, Xw)), repeat(((9, 1, 1, 7), Xw)))}
    # This is the left padding on text box
    instructions = instructions | {k: v for k, v in zip(zip(count(9 + Xw), repeat(1, Xw)), repeat((9, 1, 1, 7), Xw))}
    # This the right padding on the text box
    instructions = instructions | {(3 + Xw, 1): (2, 1, 5, 7)}
    # This is the center "artwork" being add, there is the plus 3, as x coordinates starts from 0
    instructions = instructions | {(2, 2): (0, 9, min(Lw, 23), 5)}
    if Lw > 23:
        for i in range(1, (Lw - 23) // 8 + 1):
            instructions = instructions | {(2 + 23 + 8 * (i - 1), 2): (15, 9, 8, 5)}
            # Extension of type box's input box
    for z in instructions.items():
        by = 10 if z[1][1] < 9 else 0
        print(z[1], z[0])
        print((z[1][0], z[1][1] + by, z[1][2], z[1][3]), z[0])