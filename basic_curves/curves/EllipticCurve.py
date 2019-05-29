class EllipticCurve:
    def inv_val(self, val):
        """
        Get the inverse of a given field element using the curves prime field.
        """
        return pow(val, self.mod - 2, self.mod)

    def _bf_sqrt(self, x):
        """
        Very primitive way of brute forcing a quadratic residue.
        This only works for small fields.
        :param x: Field element
        :return: sqrt(x)
        """
        for y in range(self.mod):
            if y * y % self.mod == x:
                return y

    def mul(self, point, scalar):
        """
        Do scalar multiplication Q = dP using double and add.
        """
        return self.double_and_add(point, scalar)

    def double_and_add(self, point, scalar):
        """
        Do scalar multiplication Q = dP using double and add.
        As here: https://en.wikipedia.org/wiki/Elliptic_curve_point_multiplication#Double-and-add
        """
        if scalar < 1:
            raise ValueError("Scalar must be >= 1")
        result = None
        tmp = point.copy()

        while scalar:
            if scalar & 1:
                if result is None:
                    result = tmp
                else:
                    result = self.add(result, tmp)
            scalar >>= 1
            tmp = self.add(tmp, tmp)

        return result
