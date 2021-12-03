package main

import (
	"fmt"
	"log"
	"os"
	"strconv"
	"strings"
	"time"
)

type bit struct {
	zero int
	one  int
}

func readFile(fileName string) ([]string, error) {
	data, err := os.ReadFile(fileName)
	if err != nil {
		return nil, err
	}
	parsed := string(data)
	split := strings.Split(parsed, "\n")
	return split, nil
}

func parseLines(lines []string) []bit {
	result := make([]bit, len(lines[0]))
	for _, line := range lines {
		for j, char := range line {
			if string(char) == "1" {
				result[j].one += 1
			} else if string(char) == "0" {
				result[j].zero += 1
			} else {
				panic(fmt.Sprintf("Could not parse line %v", char))
			}
		}
	}
	return result
}

func calculatePowerBasics(bs []bit) (int, int) {
	gamma, epislon := 0, 0
	for _, bit := range bs {
		gamma *= 2
		epislon *= 2
		if bit.one > bit.zero {
			gamma += 1
		} else {
			epislon += 1
		}
	}
	return gamma, epislon
}

func filter(l []string, bitPlace int, value string) []string {
	result := []string{}
	for _, s := range l {
		if string(s[bitPlace]) == value {
			result = append(result, s)
		}
	}
	return result
}

func calculateLifeMetric(lines []string, invert bool) int64 {
	for i := 0; i < len(lines[0]); i++ {
		if len(lines) == 1 {
			break
		}
		parsed := parseLines(lines)
		b := parsed[i]
		var filterChar string
		if b.one > b.zero {
			if !invert {
				filterChar = "1"
			} else {
				filterChar = "0"
			}
		} else if b.one < b.zero {
			if !invert {
				filterChar = "0"
			} else {
				filterChar = "1"
			}
		} else {
			if !invert {
				filterChar = "1"
			} else {
				filterChar = "0"
			}
		}
		lines = filter(lines, i, filterChar)
	}
	if len(lines) > 1 {
		panic("Too many lines left for calculating life metrics")
	}
	result, err := strconv.ParseInt(lines[0], 2, 64)
	if err != nil {
		panic(err)
	}
	return result
}

func calculateLifeSupport(lines []string) (int64, int64) {
	oxygen := calculateLifeMetric(lines, false)
	co2 := calculateLifeMetric(lines, true)
	return oxygen, co2
}

func main() {
	defer duration(track("total"))
	filename := "input.txt"
	lines, err := readFile(filename)
	if err != nil {
		lines, err = readFile(fmt.Sprintf("2021/day_3/%s", filename))
		if err != nil {
			panic(err)
		}
	}
	parsedLines := parseLines(lines)
	g, e := calculatePowerBasics(parsedLines) // Part 1
	fmt.Printf("Epsilon is %d, gamma is %d. The total power consumptions is %d\n", e, g, e*g)
	o, c := calculateLifeSupport(lines) // Part 2
	fmt.Printf("Oxygen is %d, CO2 is %d. The total life support is %d\n", o, c, o*c)
}

func track(msg string) (string, time.Time) {
	return msg, time.Now()
}

func duration(msg string, start time.Time) {
	log.Printf("%v: %v\n", msg, time.Since(start))
}
