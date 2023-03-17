# A-start-and-Iterative-DFS-Robot-Navigation
algorithm: one of dfs (depth-first search with cycle detection), ucs (uniform cost search), ids (iterative
deepening depth-first search), astar (A*).
heuristic: if the algorithm specified is astar, include a second argument: one of three heuristic names:
h0 (h(n) = 0), h1 (a better heuristic of your design), or h2 (an even better heuristic of your design). 
All heuristic should be admissible.

The first heuristic I used was the Manhattan distance between the robot location with the first
sample. Then I changed it to the maximum distance between robot and all samples but I did not
see any differences and the result was exactly the same.
The second heuristic I used was the maximum Manhattan distance between each two samples .
It means I calculate the distance between each two samples and then I pick the maximum
distance among them. The result in terms of the count of generated nodes and expanded nodes
got slightly better. But both ways they found the solution, and they are admissible because they
never overestimate the real cost.
