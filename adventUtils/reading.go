package adventUtils

import (
	"fmt"
	"log"
	"os"
	"strconv"
	"strings"
	"time"
)

type errorAt struct {
	index int
	err   error
}

func ReadFile(fileName string) ([]string, error) {
	data, err := os.ReadFile(fileName)
	if err != nil {
		return nil, err
	}
	parsed := string(data)
	split := strings.Split(parsed, "\n")
	return split, nil
}

func ReadFileAdvent(filename string, day int) ([]string, error) {
	lines, err := ReadFile(filename)
	if err != nil {
		lines, err = ReadFile(fmt.Sprintf("2021/day_%d/%s", day, filename))
		if err != nil {
			return nil, err
		}
	}
	return lines, nil
}

func ParseToInt(s []string) ([]int, []errorAt) {
	ints := []int{}
	errors := []errorAt{}
	for i, l := range s {
		n, err := strconv.Atoi(l)
		if err != nil {
			errors = append(errors, errorAt{index: i, err: err})
		}
		ints = append(ints, n)
	}
	if len(errors) != 0 {
		return nil, errors
	}
	return ints, nil

}

func Benchmark(f func()) {
	defer duration(track("Go took"))
	f()
}

func track(msg string) (string, time.Time) {
	return msg, time.Now()
}

func duration(msg string, start time.Time) {
	log.Printf("%v: %v\n", msg, time.Since(start))
}
