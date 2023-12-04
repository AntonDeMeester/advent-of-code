from .main import solve_part_1, solve_part_2, GameState

example_games = """Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green"""
example_suggestion = GameState(12, 14, 13)


def test_example_one():
    result = solve_part_1(example_games, example_suggestion)
    assert result == 8

def test_example_two():
    result = solve_part_2(example_games)
    assert result == 2286
