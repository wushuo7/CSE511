# helloWorld.py
# -------------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html

# Comment: This is a fairly simple Python script
    value = 0
    node = state[0]
    hasbeen = state[1]
    t = []
    nothasbeen=[]
    for corner in corners:
        if not corner in hasbeen:
            nothasbeen.append(corner)
    while len(nothasbeen)>0:
        for corner in corner:
            s = util.power(node, corner)
            t = t.append(s)
        distance, corner = min(t)
        value=distance
        node = corner
        nothasbeen.remove(corner)
    print value
