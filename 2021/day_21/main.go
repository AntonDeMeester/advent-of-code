package main

import (
	"adventofcode/adventUtils"
	"fmt"
)

type state struct {
	pos1, pos2, score1, score2 int
}

var THREE_STATE map[int]int = map[int]int{3: 1, 4: 3, 5: 6, 6: 7, 7: 6, 8: 3, 9: 1}

func parseLines(l []string) (int, int) {
	runeOne := int([]rune(l[0])[len(l[0])-1] - '0')
	runeTwo := int([]rune(l[1])[len(l[1])-1] - '0')
	return runeOne, runeTwo
}

func playRound(pos int, die int) int {
	pos += die
	pos = (pos-1)%10 + 1
	return pos
}

func playDeterministic(one, two int) int {
	sc1, sc2 := 0, 0
	i := 0
	for {
		roll := i%100 + 1
		iteration := i % 6
		if iteration < 3 {
			one = playRound(one, roll)
			if iteration == 2 {
				sc1 += one
			}
		} else {
			two = playRound(two, roll)
			if iteration == 5 {
				sc2 += two
			}
		}
		if sc1 >= 1000 {
			return sc2 * (i + 1)
		}
		if sc2 >= 1000 {
			return sc1 * (i + 1)
		}
		i++
	}
}

func godDoesntRollDice(one, two int) int {
	oldUniverse := map[state]int{state{one, two, 0, 0}: 1} // Keeping track of possible universes
	isOne := true
	allDone := false
	for !allDone {
		allDone = true
		newUniverse := map[state]int{}
		// Simulate universes for player one
		for oldState, oldV := range oldUniverse {
			if oldState.score1 >= 21 || oldState.score2 >= 21 {
				if _, ok := newUniverse[oldState]; ok {
					newUniverse[oldState] += oldV
				} else {
					newUniverse[oldState] = oldV
				}
				continue
			}
			allDone = false
			for stateChange, changeCount := range THREE_STATE {
				var oldPos int
				if isOne {
					oldPos = oldState.pos1
				} else {
					oldPos = oldState.pos2
				}
				newPos := playRound(oldPos, stateChange)
				var newState state
				if isOne {
					newState = state{newPos, oldState.pos2, oldState.score1 + newPos, oldState.score2}
				} else {
					newState = state{oldState.pos1, newPos, oldState.score1, oldState.score2 + newPos}
				}
				if _, ok := newUniverse[newState]; ok {
					newUniverse[newState] += (oldV * changeCount)
				} else {
					newUniverse[newState] = (oldV * changeCount)
				}
			}
		}
		isOne = !isOne
		oldUniverse = newUniverse
	}
	win1, win2 := 0, 0
	for state, poss := range oldUniverse {
		if state.score1 >= 21 {
			win1 += poss
		} else if state.score2 >= 21 {
			win2 += poss
		} else {
			panic("Found end state without winner")
		}
	}
	fmt.Printf("Player one wins %d times, player two wins %d times\n", win1, win2)
	if win1 > win2 {
		return win1
	} else {
		return win2
	}
}

func day21() {
	filename := "input.txt"
	rawLines, err := adventUtils.ReadFileAdvent(filename, 21)
	if err != nil {
		fmt.Errorf("%+v\n", err)
		panic(err)
	}
	pOne, pTwo := parseLines(rawLines)
	// fmt.Printf("The pattern is %+v, the image is %+v\n", pattern, image)

	// Part 1
	res1 := playDeterministic(pOne, pTwo)
	fmt.Printf("The result for part one is %d\n", res1)

	// Part 2
	einsteinsNightmare := godDoesntRollDice(pOne, pTwo)
	fmt.Printf("The number that keeps Einstein up at night is %d\n", einsteinsNightmare)

}

func main() {
	adventUtils.Benchmark(day21)
}
