<p>
    This project solves the traveling salesman problem for the thirty most populous cities in the U.S. by using a genetic algorithm.
First, five hundred randomly generated paths are made.  The next generation is made by randomly picking two paths and crossing them.
To cross the paths a random range towards the beginning of the paths is picked.  The parent who has the lowest score in this range passes that
section of the its path to its child. To fill in the rest of the child path, the remaining cities are taken from the other parent in order and
added to the child.  There is also a ten percent chance of mutation.  A mutation switches the order of two cities in the path.
Each parent is crossed twice and this process is repeated until five hundred children are made.  The algorithm proceeds
to make ten thousand generations.  The path with the lowest score in the final generation is then chosen as the solution.  The paths are
scored by calculating the distance traveled along the path.
</p>

<p>
This project also has a web component that has a map of the optimal path found.  This web page uses the Google Maps API to produce the map.
</p>