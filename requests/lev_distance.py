#!/usr/bin/env python
# -*- coding=utf-8 -*-

def lev_dist(source, target):
    if source == target:
        return 0

#words = open(test_file.txt,'r').read().split();

    # Prepare matrix
    slen, tlen = len(source), len(target)
    dist = [[0 for i in range(tlen+1)] for x in range(slen+1)]
    for i in range(slen+1):
        dist[i][0] = i
    for j in range(tlen+1):
        dist[0][j] = j

    # Counting distance
    for i in range(slen):
        for j in range(tlen):
            cost = 0 if source[i] == target[j] else 1
            dist[i+1][j+1] = min(
                            dist[i][j+1] + 1,   # deletion
                            dist[i+1][j] + 1,   # insertion
                            dist[i][j] + cost   # substitution
                        )
    return dist[-1][-1]

#print(lev_dist("расписание", "расписанье"))

def req_distance(request_words, word):

    for i in request_words:

        if lev_dist(word, i) <= 2:
            return True

    return False