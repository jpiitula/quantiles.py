from collections import Counter

# turn frequency distribution of observed numbers into a quantile list
# approximately (or is it exactly in some sense when all points are
# actually observed? need to think about it some day)

def cumsum(counts):
    '''Cumulative frequency distribution from a frequency distribution.'''

    sums = dict()
    m = 0
    for k, c in sorted(counts.items()):
        m += c
        sums[k] = m

    return sums

def quantiles(counts, *, by = 4):
    '''Return a list of the values (keys of counts) where the cumulative
    proportion reaches or passes k/by for k = 0, ..., by. These are
    approximately the quantile points.

    The default by = 4 gives quartiles aka five-number summary; the
    choice of by = 10 gives deciles aka eleven-number summary.

    '''

    def gen():
        sums = sorted(cumsum(counts).items())
        _, total = sums[-1]
        p = 0
        for k, m in sums:
            while m * by >= total * p:
                yield k
                p += 1

    return list(gen())

# to compute some tests at quartiles and deciles - how many values
# actually are strictly smaller or larger? how do they agree with the
# reported quantile values? what is proper terminology?

def quantile_report(counts, *, by = 4):
    '''Check that at least the required portion of observations falls
    in each quantile.

    For example, at least a fourth of the values is between the
    minimum and the lower quartile (point?), at least a fourth is
    between the lower quartile (point?) and median, and so on.'''

    points = quantiles(counts, by = by)

    uppers = iter(points)
    next(uppers)

    m = sum(counts.values())
    for lo, hi in zip(points, uppers):
        c = sum(counts[k] for k in counts if lo <= k <= hi)
        if by * c < m:
            print('FAIL', '{}/{} > {}'.format(m, by, c), (lo, hi))
        else:
            print('pass', '{}/{} <= {}'.format(m, by, c), (lo, hi))

if __name__ == '__main__':
    import math, random

    # test data - would have liked poisson but random has poisson not,
    # while gamma seems to have, vaguely-ish, a desired kind of shape

    data = Counter(math.ceil(random.gammavariate(3, 2))
                   for k in range(1000))

    print('Data (1000 ceiling(Gamma(3, 2)):')
    print(*('{:-2} observed {:-3} times'.format(k,c)
            for k, c in sorted(data.items())),
          sep = '\n', end = '\n\n')
    print('Quartile points:', *quantiles(data))
    quantile_report(data)
    print()
    print('Quintile points:', *quantiles(data, by = 5))
    quantile_report(data, by = 5)
    print()
    print('Decile points:', *quantiles(data, by = 10))
    quantile_report(data, by = 10)
    if True:
        print()
        print('Percentile test:')
        quantile_report(data, by = 100)
