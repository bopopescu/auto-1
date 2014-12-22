#!/usr/bin/env python
# -*- coding: utf-8 -*-



import random
def random_pick(seq,probabilities):
    x = random.uniform(0, 1)
    cumulative_probability = 0.0
    for item, item_probability in zip(seq, probabilities):
        cumulative_probability += item_probability
        if x < cumulative_probability: break
    return item



def main():
    for i in range(15):
        random_pick("abc",[0.1,0.3,0.6])

if __name__ == '__main__':
    main()
