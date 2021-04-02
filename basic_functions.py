def extend_to_32_bits(bin_instruction, signed=True):
    while len(bin_instruction) < 32:
        bin_instruction = (
            ('0' + bin_instruction) if not signed else (bin_instruction[0] + bin_instruction))
    return bin_instruction


def hex_to_bin(hex_instruction, signed=True):
    if hex_instruction[1] == 'x' or hex_instruction[1] == 'X':
        hex_instruction.replace('0x', '')
    bin_instruction = "{0:08b}".format(int(hex_instruction, 16))
    return extend_to_32_bits(bin_instruction, signed)


def twos_complement(bin_num, signed=True):
    bin_num = extend_to_32_bits(bin_num, signed)
    neg_num = ''
    for x in bin_num:
        neg_num += '1' if x == '0' else '0'
    result = ''
    carry = 1
    i = 31
    for i in range(31, -1, -1):
        digit = int(neg_num[i])
        sum = digit + carry
        carry = 1 if sum == 2 else 0
        sum = sum - (2 if carry == 1 else 0)
        result = str(sum) + result
        i -= 1
    return result


def bin_to_dec(bin_num, signed=True):
    if not signed or bin_num[0] == '0':
        return int(bin_num, 2)
    else:
        return -1 * int(twos_complement(bin_num), 2)


def dec_to_bin(dec_num):
    if dec_num >= 0:
        return bin(dec_num).replace('0b', '')[-32:]
    else:
        return twos_complement(bin(-dec_num).replace('0b', ''), signed=False)[-32:]
