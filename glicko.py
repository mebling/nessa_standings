# -*- coding: utf-8 -*-
"""
    glicko
    ~~~~~~
    The Glicko rating system.
    :copyright: (c) 2012 by Heungsub Lee
    :license: BSD, see LICENSE for more details.
"""
import math
import time


#: The actual score for win
WIN = 1.
#: The actual score for draw
DRAW = 0.5
#: The actual score for loss
LOSS = 0.


MU = 1500
SIGMA = 350
#: A constant which is used to standardize the logistic function to
#: `1/(1+exp(-x))` from `1/(1+10^(-r/400))`
Q = math.log(10) / 400


class Rating(object):

    def __init__(self, mu=MU, sigma=SIGMA):
        self.mu = mu
        self.sigma = sigma

    @property
    def impact(self):
        return (1 + (3 * (Q ** 2) * self.sigma ** 2) / math.pi ** 2) ** -0.5

    def expected_score(self, other_rating):
        return 1 / (1 + 10 ** (other_rating.impact * (self.mu - other_rating.mu) / -400.))


class Glicko(object):

    def __init__(self, mu=MU, sigma=SIGMA, period=86400):
        self.mu = mu
        self.sigma = sigma
        self.rating = Rating()

    def rate(self, series):
        d_square_inv = 0
        difference = 0
        for actual_score, other_rating in series:
            expected_score = self.rating.expected_score(other_rating)
            difference += other_rating.impact * (actual_score - expected_score)
            d_square_inv += (
                expected_score * (1 - expected_score) *
                (Q ** 2) * (other_rating.impact ** 2))
        denom = self.rating.sigma ** -2 + d_square_inv
        mu = self.rating.mu + Q / denom * difference
        self.rating = Rating(mu, math.sqrt(1. / denom))
        return self.rating
