import basic_functions


def bin_add(bin_num1, bin_num2, signed=True):
    bin_num1 = basic_functions.extend_to_32_bits(bin_num1, signed)
    bin_num2 = basic_functions.extend_to_32_bits(bin_num2, signed)
    result = ''
    carry = 0
    for i in range(31, -1, -1):
        digit_1 = int(bin_num1[i])
        digit_2 = int(bin_num2[i])
        sum = digit_1 + digit_2 + carry
        carry = 1 if sum >= 2 else 0
        sum = sum - (2 if carry == 1 else 0)
        result = str(sum) + result
    return result


def bin_sub(bin_num1, bin_num2, signed=True):
    bin_num1 = basic_functions.extend_to_32_bits(bin_num1, signed)
    bin_num2 = basic_functions.extend_to_32_bits(bin_num2, signed)
    num2_twos_comp = basic_functions.twos_complement(bin_num2)
    return bin_add(bin_num1, num2_twos_comp)


def bin_and(bin_num1, bin_num2, signed=True):
    bin_num1 = basic_functions.extend_to_32_bits(bin_num1, signed)
    bin_num2 = basic_functions.extend_to_32_bits(bin_num2, signed)
    result = ''
    for i in range(31, -1, -1):
        result = (
            ('1' + result) if bin_num1[i] == '1' and bin_num2[i] == '1' else ('0' + result))
    return result


def bin_or(bin_num1, bin_num2, signed=True):
    bin_num1 = basic_functions.extend_to_32_bits(bin_num1, signed)
    bin_num2 = basic_functions.extend_to_32_bits(bin_num2, signed)
    result = ''
    for i in range(31, -1, -1):
        result = (
            ('1' + result) if bin_num1[i] == '1' or bin_num2[i] == '1' else ('0' + result))
    return result


def bin_xor(bin_num1, bin_num2, signed=True):
    bin_num1 = basic_functions.extend_to_32_bits(bin_num1, signed)
    bin_num2 = basic_functions.extend_to_32_bits(bin_num2, signed)
    result = ''
    for i in range(31, -1, -1):
        digit_1 = int(bin_num1[i])
        digit_2 = int(bin_num2[i])
        sum = digit_1 + digit_2
        result = (('1' + result) if sum == 1 else ('0' + result))
    return result


def bin_shift_left(bin_num1, bin_num2):
    num2 = basic_functions.bin_to_dec(bin_num2, signed=False)
    if num2 >= 32:
        return basic_functions.extend_to_32_bits('0')
    else:
        result = bin_num1
        for i in range(num2):
            result = result[1:] + '0'
        return result


def bin_shift_right(bin_num1, bin_num2, arithmetic):
    num2 = basic_functions.bin_to_dec(bin_num2, signed=False)
    if num2 >= 32:
        return basic_functions.extend_to_32_bits(('0' if not arithmetic else bin_num1[0]))
    else:
        result = bin_num1
        for i in range(num2):
            result = (
                ('0' + result[:-1]) if not arithmetic else (bin_num1[0] + result[:-1]))
        return result


def bin_mul(bin_num1, bin_num2):
    num1 = basic_functions.bin_to_dec(bin_num1)
    num2 = basic_functions.bin_to_dec(bin_num2)
    signed_product = num1 * num2
    unsigned_product = abs(signed_product)
    bin_result_unsigned = basic_functions.dec_to_bin(unsigned_product)
    bin_result_signed = basic_functions.twos_complement(
        bin_result_unsigned) if signed_product < 0 else bin_result_unsigned
    return bin_result_signed


def bin_div(bin_num1, bin_num2):
    num1 = basic_functions.bin_to_dec(bin_num1)
    num2 = basic_functions.bin_to_dec(bin_num2)
    signed_quotient = num1 // num2
    unsigned_quotient = abs(num1) // abs(num2)
    bin_result_unsigned = basic_functions.dec_to_bin(unsigned_quotient)
    bin_result_signed = basic_functions.twos_complement(
        bin_result_unsigned) if signed_quotient < 0 else bin_result_unsigned
    return bin_result_signed


def bin_rem(bin_num1, bin_num2):
    num1 = basic_functions.bin_to_dec(bin_num1)
    num2 = basic_functions.bin_to_dec(bin_num2)
    unsigned_rem = abs(num1) % abs(num2)
    bin_result_unsigned = basic_functions.dec_to_bin(unsigned_rem)
    bin_result_signed = basic_functions.twos_complement(
        bin_result_unsigned) if num1 < 0 else bin_result_unsigned
    return bin_result_signed
