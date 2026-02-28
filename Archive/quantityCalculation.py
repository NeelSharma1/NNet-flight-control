# THIS FILE USES IMPERIAL UNITS NOT METRIC

import math

r = 20925722
g0 = 32.2
R = 1716
sltemp = 518.67
slpressure = 2116.22
sldensity = 0.002377
a1 = -6.5e-3 / 3.2808399 * 1.8
a2 = 3e-3 / 3.2808399 * 1.8


# determines the a value given a current height (does not return 0, since it's not necessary later in the code)
def currA(h):
    return a2 if h >= 82349 else a1


def temp(h):
    # temp = sltemp  # sets base temp
    # while h > 0:
    #     temp += currA(h)  # for every foot, increment by whatever the current A value is
    #     if 36089 < h < 82349:  # this statement is just to skip the ~45000 feet where a = 0
    #         h = 36090
    #     h -= 1
    # return temp
    return sltemp + (h - max(0, h - 36089)) * a1 + max(0, h - 82349) * a2


def pressure(h):
    # # Chained if statements work so that if the height is above a threshold, it will max out the threshold pressure to
    # # create the baseline for the next threshold
    # p = slpressure  # sets base sea level pressure
    # if h > 36089:
    #     p *= (temp(36089) / sltemp) ** (-g0 / (currA(0) * R))
    #     # baseline made for isothermal
    #     if h > 82349:
    #         p *= math.e ** ((-g0 / (R * temp(82349))) * (82349 - 36089))
    #         # baseline made for last gradient
    #         p *= (temp(h) / temp(36089)) ** (-g0 / (currA(h) * R))
    #     else:
    #         p *= math.e ** ((-g0 / (R * temp(h))) * (h - 36089))
    # else:
    #     p *= (temp(h) / sltemp) ** (-g0 / (currA(0) * R))
    # return p
    return slpressure * (temp(min(h, 36089)) / sltemp) ** (-g0 / (a1 * R)) * math.e ** (
                (-g0 / (R * temp(82349))) * max(min(h - 36089, 46260), 0)) * (temp(max(h, 82349)) / temp(82349)) ** (
                -g0 / (a2 * R))

def density(h):
    # This method uses the same logic as the pressure method, but with the slightly modified formula necessary for
    # pressure to get exactly the right value.
    # p = sldensity
    # if h > 36089:
    #     p *= (temp(36089) / sltemp) ** (-g0 / (currA(0) * R) - 1)
    #     if h > 82349:
    #         p *= math.e ** ((-g0 / (R * temp(82349))) * (82349 - 36089))
    #         p *= (temp(h) / temp(36089)) ** (-g0 / (currA(h) * R) - 1)
    #     else:
    #         p *= math.e ** ((-g0 / (R * temp(h))) * (h - 36089))
    # else:
    #     p *= (temp(h) / sltemp) ** (-g0 / (currA(0) * R) - 1)
    # return p
    return sldensity * (temp(min(h, 36089)) / sltemp) ** (-g0 / (a1 * R) - 1) * math.e ** (
                    (-g0 / (R * temp(82349))) * max(min(h - 36089, 46260), 0)) * (temp(max(h, 82349)) / temp(82349)) ** (
                    -g0 / (a2 * R) - 1)


def sos(h):
    return (1.4 * R * temp(h)) ** 0.5  # uses the gamma constant and formula sqrt(gamma * R * T) for speed of sound

if __name__ == "__main__":
    print(density(91.44) * 16.0185)
