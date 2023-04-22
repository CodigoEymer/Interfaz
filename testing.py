def intersection_point():
    vertices = [(1,2),(2,3),(3,4),(4,5),(5,6)]
    p=len(vertices)
    new_vertices = []
    print(new_vertices)
    print(vertices)
    if vertices[0][1] <= vertices[1][1]:
        for index in range(p):
            print(index)
            if index > 0:
                new_vertices.append(vertices[p-(index)])
                print(new_vertices)
                print(vertices)
            else:
                new_vertices.append(vertices[0])
    return new_vertices
intersect = intersection_point()
