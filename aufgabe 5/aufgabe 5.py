'''

http://andrew.gibiansky.com/blog/machine-learning/speech-recognition-neural-networks/

https://gab41.lab41.org/speech-recognition-you-down-with-ctc-8d3b558943f0

https://www.cs.toronto.edu/~graves/preprint.pdf

'''

import numpy as np
import matplotlib.pyplot as plt


def ctc(prob, seq):

    # Thus, instead of considering a label ℓ, we consider a modified label L,
    # which is just ℓ with blanks inserted between all letters, as well as at the beginning and end.
    L = 2 * len(seq) + 1    # length of sequence [9]
    T = prob.shape[1]       # timesteps [1, ..., 12]
    blank = 0

    a = np.zeros((L, T))
    b = np.zeros((L, T))

    a[0, 0] = prob[blank, 0]
    a[1, 0] = prob[seq[0], 0]

    c = np.sum(a[:, 0])
    a[:, 0] /= c

    forward = np.log(c)

    for t in range(1, T):
        start = max(0, L - 2 * (T - t))
        end = min(2 * t + 2, L)
        for s in range(start, L):
            l = (s - 1) / 2

            if(s % 2 == 0):
                if(s == 0):
                    a[s, t] = a[s, t - 1] * prob[blank, t]
                else:
                    a[s, t] = (a[s, t - 1] + a[s - 1, t - 1]) * prob[blank, t]
            elif(s == 1 or seq[l] == seq[l - 1]):
                a[s, t] = (a[s, t - 1] + a[s - 1, t - 1]) * prob[seq[l], t]
            else:
                a[s, t] = (a[s, t - 1] + a[s - 1, t - 1] + a[s-2, t - 1]) * prob[seq[l], t]

        c = np.sum(a[start:end, t])
        a[start:end, t] /= c
        forward += np.log(c)

        print(forward)

    pass


def main():

    '''
    equal distribution:

    ykt     t=1  t=2  t=3  t=4  t=5  t=6  t=7  t=8  t=9  t=10 t=11 t=12
    k=ε     0.25 0.25 0.25 0.25 0.25 0.25 0.25 0.25 0.25 0.25 0.25 0.25
    k=“a“   0.25 0.25 0.25 0.25 0.25 0.25 0.25 0.25 0.25 0.25 0.25 0.25
    k=“b“   0.25 0.25 0.25 0.25 0.25 0.25 0.25 0.25 0.25 0.25 0.25 0.25
    k=“c“   0.25 0.25 0.25 0.25 0.25 0.25 0.25 0.25 0.25 0.25 0.25 0.25


    weighted distribution:

    ykt     t=1  t=2  t=3 t=4 t=5 t=6 t=7 t=8  t=9 t=10 t=11 t=12
    k=ε     0.25 0.25 0.0 0.0 0.0 0.5 0.5 0.25 0.0 0.0  0.25 0.25
    k=“a“   0.75 0.75 0.5 0.5 0.0 0.0 0.0 0.0  0.0 0.0  0.0  0.0
    k=“b“   0.0  0.0  0.5 0.5 1.0 0.5 0.5 0.5  0.5 0.5  0.25 0.0
    k=“c“   0.0  0.0  0.0 0.0 0.0 0.0 0.0 0.25 0.5 0.5  0.5  0.75
    '''

    seq = 'abbc'

    probEqual = np.array([
        [0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25],
        [0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25],
        [0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25],
        [0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25]
    ])

    probWeighted = np.array([
        [.25, .25, .0, .0, .0, .5, .5, .25, .0, .0, .25, .25],
        [.75, .75, .5, .5, .0, .0, .0,  .0, .0, .0,  .0,  .0],
        [ .0,  .0, .5, .5, 1., .5, .5,  .5, .5, .5, .25,  .0],
        [ .0,  .0, .0, .0, .0, .0, .0, .25, .5, .5,  .5, .75],
    ])

    ctc(probEqual, seq)

    pass


if __name__ == '__main__':
    main()