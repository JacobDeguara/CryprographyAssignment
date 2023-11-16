class MT19937Cracker:
    def __init__(self) -> None:
        self.list_of_seen = list()
        self.counter = 0

    def crack(self, random: int):
        if self.counter == 624:
            print("-- THATS ENOUGH RANDOM NUMBERS --")
            return
        rand_val = self._untemper(int(random))
        self.list_of_seen.append(rand_val)
        self.counter += 1

    def get_next(self):
        next_rand = self.list_of_seen[-624 + 397] ^ self.timesA(
            self._upper(self.list_of_seen[-624])
            | self._lower(self.list_of_seen[-624 + 1])
        )
        self.list_of_seen.append(next_rand)
        predicted = self._temper(next_rand)
        return predicted

    def _undo_xor_rshift(self, x, shift):
        """reverses the operation x ^= (x >> shift)"""
        result = x
        for shift_amount in range(shift, 32, shift):
            result ^= x >> shift_amount
        return result

    def _undo_xor_lshiftmask(self, x, shift, mask):
        """reverses the operation x ^= ((x << shift) & mask)"""
        window = (1 << shift) - 1
        for _ in range(32 // shift):
            x ^= ((window & x) << shift) & mask
            window <<= shift
        return x

    def _temper(self, x):
        """tempers the value to improve k-distribution properties"""
        x ^= x >> 11
        x ^= (x << 7) & 0x9D2C5680
        x ^= (x << 15) & 0xEFC60000
        x ^= x >> 18
        return x

    def _untemper(self, x):
        """reverses the tempering operation"""
        x = self._undo_xor_rshift(x, 18)
        x = self._undo_xor_lshiftmask(x, 15, 0xEFC60000)
        x = self._undo_xor_lshiftmask(x, 7, 0x9D2C5680)
        x = self._undo_xor_rshift(x, 11)
        return x

    def _upper(self, x):
        """return the upper (w - r) bits of x"""
        return x & ((1 << 32) - (1 << 31))

    def _lower(self, x):
        """return the lower r bits of x"""
        return x & ((1 << 31) - 1)

    def timesA(self, x):
        """performs the equivalent of x*A"""
        if x & 1:
            return (x >> 1) ^ 0x9908B0DF
        else:
            return x >> 1


if __name__ == "__main__":
    import time

    from MT19937.RandomClass import Random

    mt = Random(int(time.time()))
    cracker_mt = MT19937Cracker()

    for _ in range(624):
        cracker_mt.crack(mt.randint(0, 2**32))

    print(
        "Guessing next 32000 random bits success rate: {}%".format(
            sum([cracker_mt.get_next() == mt.randint(0, 2**32) for x in range(1000)])
            / 10
        )
    )
