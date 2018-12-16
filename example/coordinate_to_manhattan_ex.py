from mapAPI.v2.transform_v2 import CoordinateToManhattan

if __name__ == '__main__':
    coordinate_to_manhattan = CoordinateToManhattan()
    distance = {'BUS': 0.002, 'CROSSWALK': 0.001, 'SUBWAY': 0.015, 'POPULATION': 0.015}

    # list type data
    coordinate_a = [[37.5874992, 126.9963989]]

    # dict type data
    coordinate_b = {'lat': [37.5874992], 'lng': [126.9963989]}

    result_a = coordinate_to_manhattan(coordinate_a, distance)
    result_b = coordinate_to_manhattan(coordinate_b, distance)

