package main

import (
	"adventofcode/adventUtils"
	"fmt"
	"strconv"
	"strings"
)

func parseLine(l []string) []int {
	rawNumbers := strings.Split(l[0], ",")
	res := []int{}
	for _, s := range rawNumbers {
		n, err := strconv.Atoi(s)
		if err != nil {
			panic(err)
		}
		res = append(res, n)
	}
	return res
}

func parseToMap(f []int) map[int]int64 {
	m := map[int]int64{}
	for _, d := range f {
		if _, ok := m[d]; ok {
			m[d] += 1
		} else {
			m[d] = 1
		}
	}
	return m
}

func passDay(fish []int) []int {
	res := []int{}
	extra := 0
	for _, f := range fish {
		if f == 0 {
			res = append(res, 6)
			extra += 1
		} else {
			res = append(res, f-1)
		}
	}
	for i := 0; i < extra; i++ {
		res = append(res, 8)
	}
	return res
}

func passDays(fish []int, days int) []int {
	for i := 0; i < days; i++ {
		fish = passDay(fish)
	}
	return fish
}

func passDayCount(fish map[int]int64) map[int]int64 {
	newMap := map[int]int64{}
	for i := 8; i >= 0; i-- {
		if i == 0 {
			newMap[6] += fish[0]
			newMap[8] = fish[0]
		} else {
			newMap[i-1] = fish[i]
		}
	}
	return newMap
}

func countFishAfterDays(fish []int, days int) int64 {
	mappedFish := parseToMap(fish)
	for i := 0; i < days; i++ {
		mappedFish = passDayCount(mappedFish)
	}
	var res int64 = 0
	for _, c := range mappedFish {
		res += c
	}
	return res
}

func day_6() {
	filename := "input_easy.txt"
	rawLines, err := adventUtils.ReadFileAdvent(filename, 6)
	if err != nil {
		fmt.Errorf("%+v\n", err)
		panic(err)
	}
	init := parseLine(rawLines)

	// Part 1
	after80Days := countFishAfterDays(init, 80)
	fmt.Printf("After 80 days there are %d fish.\n", after80Days)

	// Part 2
	after256Days := countFishAfterDays(init, 256)
	fmt.Printf("After 256 days there are %d fish \n", after256Days)

}

func main() {
	adventUtils.Benchmark(day_6)
}
