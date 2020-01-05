import enum
import matplotlib.pyplot as plt


class TypeSeq(enum.Enum):
    VAN_DER_CORPUT = 1


class SequenceMethod:
    def __init__(self, base, dimension: int):
        self.base = base
        self.d = dimension

    def generate_number(self, base: int):
        pass

    def generate_sequence(self, number_to, number_from=1, number_list=None):
        pass


class SequenceGenerator:
    def __init__(self, seq_type: TypeSeq, base: int):
        self.type = seq_type
        self.base = base

    def generate_number(self, n):
        a = []
        if self.type == TypeSeq.VAN_DER_CORPUT:
            count = 1
            current_value = n
            while (current_value % self.base != 0) | (int(current_value/self.base) != 0):
                temp_a_1 = current_value % self.base
                current_value = int(current_value/self.base)
                a.append(temp_a_1*(1/(self.base**count)))
                count = count + 1
            return sum(a)

    def generate_sequence(self, seq_type: TypeSeq, number_to, number_from=1, number_list=None):
        seq = []
        if seq_type == TypeSeq.VAN_DER_CORPUT:
            if number_list is not None:
                for k in number_list:
                    seq.append(self.generate_number(k))
            else:
                for i in range(number_from, number_to, 1):
                    seq.append(self.generate_number(i))
            return seq


if __name__ == '__main__':
    vdc = SequenceGenerator(TypeSeq.VAN_DER_CORPUT, 2)
    vdc2 = SequenceGenerator(TypeSeq.VAN_DER_CORPUT, 3)
    l1 = []
    l2 = []
    for i in range(1, 500):
        l1.append(vdc.generate_number(i))
        l2.append(vdc2.generate_number(i))

    plt.scatter(l1, l2)
    plt.show()