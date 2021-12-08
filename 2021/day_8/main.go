package main

import (
	"adventofcode/adventUtils"
	"fmt"
	"sort"
	"strings"
)

type pattern struct {
	signals []string
	output  []string
}

func parseLines(l []string) []pattern {
	res := []pattern{}
	for _, i := range l {
		res = append(res, parseLine(i))
	}
	return res
}

func parseLine(i string) pattern {
	split := strings.Split(i, " | ")
	return pattern{
		signals: strings.Split(split[0], " "),
		output:  strings.Split(split[1], " "),
	}
}

func count1478Occurence(p pattern) int {
	res := 0
	for _, o := range p.output {
		if len(o) == 2 || len(o) == 4 || len(o) == 3 || len(o) == 7 {
			res += 1
		}
	}
	return res
}

func partOne(ps []pattern) int {
	res := 0
	for _, p := range ps {
		res += count1478Occurence(p)
	}
	return res
}

func sortString(w string) string {
	s := strings.Split(w, "")
	sort.Strings(s)
	return strings.Join(s, "")
}

func sortStrings(sl []string) []string {
	res := []string{}
	for _, s := range sl {
		res = append(res, sortString(s))
	}
	return res
}

func partTwo(ps []pattern) int {
	res := 0
	for _, p := range ps {
		p = pattern{signals: sortStrings(p.signals), output: sortStrings(p.output)}
		sols := figureOutDigits(p.signals)
		res += makeNumber(p.output, sols)
	}
	return res

}

func getOverlap(one string, two string) (int, int) {
	// Number of letters in one but not two
	// Number of letters in two but not one
	var oneNotTwo, twoNotOne int
	for _, c := range one {
		if !strings.ContainsRune(two, c) {
			oneNotTwo += 1
		}
	}
	for _, c := range two {
		if !strings.ContainsRune(one, c) {
			twoNotOne += 1
		}
	}
	return oneNotTwo, twoNotOne
}

func figureOutDigits(signals []string) map[string]int {
	var sols [10]string
	// Getting straigh solutions
	notFound := []string{}
	for _, s := range signals {
		if len(s) == 2 {
			sols[1] = s
		} else if len(s) == 4 {
			sols[4] = s
		} else if len(s) == 3 {
			sols[7] = s
		} else if len(s) == 7 {
			sols[8] = s
		} else {
			notFound = append(notFound, s)
		}
	}
	// Get second order solutions
	// 3 based on 7 (2 extra as 7)
	// 9 based on 4 (2 extra as 4)
	// 0 based on 7 (0 has 3 more)
	// 6 based on 7( 6 has 4 not in 4, 4 has 1 not in 6)
	signals = notFound
	notFound = []string{}
	for _, s := range signals {
		if i, j := getOverlap(s, sols[7]); i == 2 && j == 0 {
			sols[3] = s
		} else if i, j := getOverlap(s, sols[4]); i == 2 && j == 0 {
			sols[9] = s
		} else if i, j := getOverlap(s, sols[7]); i == 3 && j == 0 {
			sols[0] = s
		} else if i, j := getOverlap(s, sols[7]); i == 4 && j == 1 {
			sols[6] = s
		} else {
			notFound = append(notFound, s)
		}
	}

	// Third order
	// 5 based on 9 (9 has 1 more)
	// 2 based on 4 (2 overlap, 3 in 2 not in 4, 2 in 4 not in 2)
	signals = notFound
	for _, s := range signals {
		if i, j := getOverlap(s, sols[9]); i == 0 && j == 1 {
			sols[5] = s
		} else if i, j := getOverlap(s, sols[4]); i == 3 && j == 2 {
			sols[2] = s
		}
	}

	var res map[string]int = map[string]int{}
	for i, v := range sols {
		res[v] = i
	}

	return res
}

func makeNumber(o []string, s map[string]int) int {
	res := 0
	for _, d := range o {
		res *= 10
		i, ok := s[d]
		if !ok {
			panic(fmt.Sprintf("Could not find %s in %+v", d, s))
		}
		res += i
	}
	return res
}

func day_8() {
	filename := "input.txt"
	rawLines, err := adventUtils.ReadFileAdvent(filename, 8)
	if err != nil {
		fmt.Errorf("%+v\n", err)
		panic(err)
	}
	patterns := parseLines(rawLines)

	// Part 1
	count1478 := partOne(patterns)
	fmt.Printf("The number of one, four, seven or eights is %d\n", count1478)

	// // Part 2
	realNumber := partTwo(patterns)
	fmt.Printf("The sum of all real numbers is %d\n", realNumber)

}

func main() {
	adventUtils.Benchmark(day_8)
}
