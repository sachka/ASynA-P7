from collections import defaultdict


class SparseWeightVector:

    def __init__(self):

        self.weights = defaultdict(float)

    def __call__(self, x_key, y_key):
        """
        This returns the weight of a feature couple (x,y)
        Enables an  x = w('a','b') syntax.

        @param x_key: a tuple of observed values
        @param y_key: a string being a class name
        @return : the weight of this feature
        """
        return self.weights[(x_key, y_key)]

    def dot(self, xvec_keys, y_key):
        """
        This computes the dot product : w . Phi(x,y).
        Phi(x,y) is implicitly  generated by the function given (x,y)
        @param xvec_keys: a list (vector) of hashable x values
        @param y_key    : a y class name
        @return  w . Phi(x,y)
        """
        return sum([self.weights[(x_key, y_key)] for x_key in xvec_keys])

    @staticmethod
    def code_phi(xvec_keys, ykey):
        """
        Explictly generates a sparse boolean Phi(x,y) vector from (x,y) values
        @param xvec_keys:  a list of symbols
        @param ykey: a y class name
        Codes the vector x of symbolic tuples for class y on a sparse vector
        """
        w = SparseWeightVector()
        for xkey in xvec_keys:
            w[(xkey, ykey)] += 1.0
        return w

    def __getitem__(self, key):
        """
        This returns the weight of feature couple (x,y) given as value.
        Enables the 'x = w[]' syntax.

        @param key: a couple (x,y) of observed and class value
        @return : the weight of this feature
        """
        return self.weights[tuple(key)]

    def __setitem__(self, key, value):
        """
        This sets the weight of a feature couple (x,y) given as key.
        Enables the 'w[] = ' syntax.
        @param key:   a couple (x,y) of observed value and class value
        @param value: a real
        """
        self.weights[key] = value

    def __add__(self, other):

        weights = self.weights.copy()
        for key, value in other.weights.items():
            weights[key] += value
        w = SparseWeightVector()
        w.weights = weights
        return w

    def __sub__(self, other):

        weights = self.weights.copy()
        for key, value in other.weights.items():
            weights[key] -= value
        w = SparseWeightVector()
        w.weights = weights
        return w

    def __mul__(self, scalar):

        weights = self.weights.copy()
        for key, value in self.weights.items():
            weights[key] *= scalar
        w = SparseWeightVector()
        w.weights = weights
        return w

    def __rmul__(self, scalar):
        return self.__mul__(scalar)

    def __truediv__(self, scalar):
        weights = self.weights.copy()
        for key, value in self.weights.items():
            weights[key] /= scalar
        w = SparseWeightVector()
        w.weights = weights
        return w

    def __iadd__(self, other):
        """
        Sparse Vector inplace addition. Enables the '+=' operator.
        @param  other: a  SparseVectorModel object
        """
        for key, value in other.weights.items():
            self.weights[key] += value
        return self

    def __isub__(self, other):
        """
        Sparse Vector inplace substraction. Enables the '-=' operator.
        @param  other: a  SparseVectorModel object
        """
        for key, value in other.weights.items():
            self.weights[key] -= value
        return self

    def __neg__(self):
        """
        returns -w
        """
        w = SparseWeightVector()
        for key, value in self.weights.items():
            w.weights[key] = -value
        return w

    def load(self, istream):
        """
        Loads a model parameters from a text stream
        @param istream: an opened text stream
        """
        self.weights = defaultdict(int)
        for line in istream:
            fields = line.split()
            key, value = tuple(fields[:-1]), float(fields[-1])
            self.weights[key] = value

    def save(self, ostream):
        """
        Saves model parameters to a text stream
        @param ostream: an opened text output stream
                """
        for key, value in self.weights.items():
            print(' '.join(list(key) + [str(value)]), file=ostream)

    def __str__(self):
        """
        Pretty prints the weights vector on std output.
        May crash if vector is too wide/full
        """
        s = ''
        for key, value in self.weights.items():
            X, Y = key
            if isinstance(X, tuple):
                s += 'phi(%s,%s) = 1 : w = %f\n' % ('&'.join(X), Y, value)
            else:
                s += 'phi(%s,%s) = 1 : w = %f\n' % (key, Y, value)
        return s


if __name__ == '__main__':

    # Simple usage example
    X = ['a', 'b', 'c']
    X = list(zip(X, X[1:]))
    print(X)
    w = SparseWeightVector()
    pred = SparseWeightVector.code_phi(X, 'A')
    ref = SparseWeightVector.code_phi(X, 'B')
    delta = (ref - pred) * 0.7
    w += delta
    print(delta)
    print(w)
    print(w.dot(X, 'A'))  # dot product : W . Phi(X,A)
    print(w.dot(X, 'B'))  # dot product : W . Phi(X,B)
