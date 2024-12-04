def dec2bin(dec):
    binN = [0] * 9
    idx = 0
    while dec != 0:
        binN[idx] = dec % 2
        dec //= 2
        idx += 1
    return binN
