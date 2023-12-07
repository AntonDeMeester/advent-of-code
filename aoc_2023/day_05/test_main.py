from .main import solve_part_1, solve_part_2

almanac = """seeds: 79 14 55 13

seed-to-soil map:
50 98 2
52 50 48

soil-to-fertilizer map:
0 15 37
37 52 2
39 0 15

fertilizer-to-water map:
49 53 8
0 11 42
42 0 7
57 7 4

water-to-light map:
88 18 7
18 25 70

light-to-temperature map:
45 77 23
81 45 19
68 64 13

temperature-to-humidity map:
0 69 1
1 0 69

humidity-to-location map:
60 56 37
56 93 4"""


def test_example_one():
    result = solve_part_1(almanac)
    assert result == 35


def test_example_two():
    result = solve_part_2(almanac)
    assert result == 46



"""
EXAMPLE 

TEMP TO HUMIDITY
0 1 2 .... 67 68 69 70 ...
1 2 3 .... 68 69 00 70 ...

HUMIDITY TO LOCATION
0 1 .... 55 56 57 58 ... 91 92 93 94 95 96 97 98 99 ...
0 1 .... 55 60 61 62 ... 95 96 56 57 58 59 97 98 99 ...

==> 
TEMP 0 1 2 ... 54 55 56 57 ... 67 68 69 70 ... 91 92 93 94 95 96 97 98 99 ....
HUMI 1 2 3 ... 55 56 57 58 ... 68 69 00 70 ... 91 92 93 94 95 96 97 98 99 ....
LOCA 1 2 3 ... 55 60 61 62 ... 72 73 00 74 ... 95 96 56 57 58 59 97 98 99 .... 

END RESULT
TEMP TO LOCATION
 1  0 54
60 55 14
 0 69  1
74 70 23
56 93  4
"""