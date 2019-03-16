# -*- coding: utf-8 -*-


def sec2time(sec):
    """ Convert seconds to '#D days#, HH:MM:SS.FFF' """
    if hasattr(sec, '__len__'):
        return [sec2time(s) for s in sec]
    m, s = divmod(sec, 60)
    h, m = divmod(m, 60)
    # d, h = divmod(h, 24)
    pattern = r'%02d时%02d分%02d秒'
    # print(pattern % (h, m, s))
    return pattern % (h, m, s)


def time2sec(t):
    if t != '0':
        h, m, s = t.strip().split(":")
        return int(h) * 3600 + int(m) * 60 + int(s)
    else:
        return 0


# time2sec('12:33:54')
