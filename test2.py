def closer(a, b, c, by=1):
    '''This function returns what the effect of by will be on +/- it
    to b, this returns which operation should be performed to get the closetest
    to a or c'''
    smaller = min(a, c)
    larger = max(a, c)
    minus = [(b - by) - smaller, b - by]
    addition = [larger - (b + by), b + by]
    if min(minus[0], addition[0]) == minus[0]:
        return minus[1]
    else:
        return addition[1]

print(closer(10, 16, 20, 1))