import itertools

def zbits(n, k):
    """
    :param n: binary strings of length
    :param k: k zero bits
    :return: all binary strings of length n that contain k zero bits, one per line.
    """

    # specify the number of zero
    num_zero = "0" * k
    # specify the number of one
    num_one = "1" * (n-k)

    string = num_zero + num_one

    strings_list = set()

    # use itertools print the permutations of the binary string
    for i in itertools.permutations(string, n):
        strings_list.add(''.join(i))

    return strings_list

if __name__ == '__main__':
    assert zbits(4, 3) == {'0100', '0001', '0010', '1000'}
    assert zbits(4, 1) == {'0111', '1011', '1101', '1110'}
    assert zbits(5, 4) == {'00001', '00100', '01000', '10000', '00010'}



