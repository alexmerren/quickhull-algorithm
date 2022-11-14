import numpy as np
import matplotlib.pyplot as plt
from math import dist, atan2

def cross_product(point1, point2, point3):
    """
    cross_product calculates the angle of two intersecting lines, point1 -> point2,
    and point1 -> point3.

    returns:
        angle (int): zero means on the line, negative means to the left,
        positive means to the right.
    """
    return (point2[0]-point1[0])*(point3[1]-point1[1]) - (point3[0]-point1[0])*(point2[1]-point1[1])

def find_coordinates_above_and_below_line(coordinates, line_start, line_end):
    """
    find_coordinates_above_and_below uses the cross product of three points to
    create two sets of points of above and below the line point1 -> point2.

    returns:
        above_line (list): List of points that are above the line.
        below_line (list): List of points that are below the line.
    """
    above_line, below_line = [], []
    for point in coordinates:
        angle = cross_product(line_start, line_end, point)
        if angle == 0 or point == line_start or point == line_end:
            pass
        if angle > 0:
            above_line.append(point)
        else:
            below_line.append(point)

    return above_line, below_line

def find_leftmost_and_rightmost(coordinates):
    """
    find_leftmost_and_rightmost returns the coordinates with the max and min
    x-value respectively.

    returns:
        leftmost (list): Coordinate with the least x-value.
        rightmost (list): Coordinate with the most x-value.
    """
    leftmost = min(coordinates, key=lambda x: (x[0]))
    rightmost = max(coordinates, key=lambda x: (x[0]))
    return leftmost, rightmost

def distance_from_line_to_point(line_start, line_end, point):
    """
    distance_from_line_to_point finds the perpendicular distance from a point
    to a given line.
    """
    line_distance = dist(line_start, line_end)
    angle = cross_product(line_start, line_end, point)
    return angle/line_distance

def farthest_point_from_line(coordinates, line_start, line_end):
    """
    farthest_point_from_line finds a point with the maximum distance from a
    line given from a set of coordinates.

    returns:
        farthest_point (list): A point farthest from a given line.
    """
    distances = []
    for point in coordinates:
        distances.append(distance_from_line_to_point(line_start, line_end, point))
    index = distances.index(max(distances))
    return coordinates[index]

def find_hull(subset_of_coordinates, line_start, line_end):
    """ 
    find_hull finds a convex hull of points above a lint by recursively
    creating triangles with the farthest point from a line.
    
    returns:
        convex_hull (list): A list of points that are a convex hull of a set of
        points above a line.
    """
    # This is the base case of the recursion. This is 'hit' if there are no
    # more points that are available to be part of the convex hull.
    if not subset_of_coordinates:
        return []

    # Find the farthest away points from that line. This point must be part of
    # the convex hull of the points.
    farthest_point = farthest_point_from_line(subset_of_coordinates, line_start, line_end)
    convex_hull = [farthest_point]

    # Create two subsets of the coordinates, one containing coordinates above
    # the line line_start -> farthest_point. The other subset contains
    # coordinates above farthest_point -> line_end.
    coordinates_above_right_side = find_coordinates_above_and_below_line(subset_of_coordinates, line_start, farthest_point)[0]
    coordinates_above_left_side = find_coordinates_above_and_below_line(subset_of_coordinates, farthest_point, line_end)[0]

    # Recursively calculate the hulls of the subsets we just created.
    right_hull = find_hull(coordinates_above_right_side, line_start, farthest_point)
    left_hull = find_hull(coordinates_above_left_side, farthest_point, line_end)

    return convex_hull + right_hull + left_hull

def quick_hull(coordinates):
    """
    quick_hull finds the convex hull of a set of points using the quickhull algorithm.

    returns:
        convex_hull (list): A convex hull of the list of coordinates.
    """
    # Find the leftmost and rightmost coordinates by their x-value
    leftmost, rightmost = find_leftmost_and_rightmost(coordinates)

    # Create a set of points that are above and below line created by leftmost
    # and rightmost.
    coords_above_line, coords_below_line = find_coordinates_above_and_below_line(coordinates, leftmost, rightmost)

    # Find the convex hull of the set of coordinates above and below the line.
    above_convex_hull = find_hull(coords_above_line, leftmost, rightmost)
    below_convex_hull = find_hull(coords_below_line, rightmost, leftmost)

    return [leftmost] + above_convex_hull + below_convex_hull + [rightmost]

def generate_coordinates():
    """
    generate_coordinates is a helper function to create a set of random points.

    reurns:
        coordinates (list): A list of random x and y coordinate pairs.
    """
    x_coordinates = np.random.randint(0, 50, 20)
    y_coordinates = np.random.randint(0, 50, 20)
    return [[item[0], item[1]] for item in zip(x_coordinates, y_coordinates)] 

def plot_convex_hull(coordinates, convex_hull):
    """
    plot_convex_hull is a helper function to display the computed convex hull
    of a set of coordinates using the quickhull algorithm.
    """
    x_coordinates, y_coordinates = [item for item in zip(*coordinates)]

    # Define the center of the coordinates to find the clockwise order of the
    # points. We use the atan2 function to find the angle from the center to
    # the points. Add the first point in clockwise order to the end to finish
    # the convex hull.
    x_center, y_center  = sum(x_coordinates)/len(x_coordinates), sum(y_coordinates)/len(y_coordinates)
    convex_hull.sort(key=lambda x: (atan2(x[1]-y_center, x[0]-x_center)))
    convex_hull.append(convex_hull[0])
    x_convex_hull, y_convex_hull = [item for item in zip(*convex_hull)]

    # Plot the coordinates inside the convex hull as red points, and
    # coordinates that create the convex hull as blue points, connected with a
    # blue line.
    plt.plot(x_coordinates, y_coordinates, "ro")
    plt.plot(x_convex_hull, y_convex_hull, "bo-")
    plt.show()

def main():
    # Generate a random amount of coordinates to compute the convex hull of.
    coordinates = generate_coordinates()

    # Compute the convex hull of the coordinates using the quickhull algorithm.
    convex_hull = quick_hull(coordinates)
    plot_convex_hull(coordinates, convex_hull)

if __name__ == "__main__":
    main()
