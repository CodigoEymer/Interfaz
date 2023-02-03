import json

if __name__ == "__main__":
    coords_dict = json.loads("""{"type":"Feature","properties":{},"geometry":{"type":"Polygon","coordinates":[[[-76.51896,3.442056],[-76.515098,3.434174],[-76.528187,3.432546],[-76.51896,3.442056]]]}}""")
    coords= coords_dict['geometry']['coordinates'][0]
    print(coords)


