package main

import (
	"adventofcode/adventUtils"
	"fmt"
	"strings"
)

var DIRECTIONS = [8][2]int{{1, 0}, {1, 1}, {0, 1}, {-1, 1}, {-1, 0}, {-1, -1}, {0, -1}, {1, -1}}

func addToMap(m map[string][]string, k string, v string) map[string][]string {
	_, present := m[k]
	if present {
		m[k] = append(m[k], v)
	} else {
		m[k] = []string{v}
	}
	return m
}

func parseLines(l []string) map[string][]string {
	res := map[string][]string{}
	for _, line := range l {
		split := strings.Split(line, "-")
		if split[0] != "end" && split[1] != "start" {
			res = addToMap(res, split[0], split[1])
		}
		if split[0] != "start" && split[1] != "end" {
			res = addToMap(res, split[1], split[0])
		}
	}
	return res
}

func contains(l []string, v string) bool {
	for _, s := range l {
		if s == v {
			return true
		}
	}
	return false
}

func sliceEqual(a []string, b []string) bool {
	if len(a) != len(b) {
		return false
	}
	for i := 0; i < len(a); i++ {
		if a[i] != b[i] {
			return false
		}
	}
	return true
}

func appendUnique(paths [][]string, n []string) [][]string {
	for _, p := range paths {
		if sliceEqual(p, n) {
			return paths
		}
	}
	return append(paths, n)
}

func findPath(current string, caves map[string][]string, visited []string) int {
	if current == "end" {
		return 1
	}
	next, ok := caves[current]
	if !ok {
		return 0
	}
	res := 0
	for _, p := range next {
		if contains(visited, p) {
			continue
		}
		var nextVisited []string
		if p != strings.ToUpper(p) {
			nextVisited = append(visited, p)
		} else {
			nextVisited = visited
		}
		res += findPath(p, caves, nextVisited)
	}
	return res
}

func findAllPaths(caves map[string][]string) int {
	return findPath("start", caves, []string{})
}

func findPathRepeatOnce(currentPath []string, caves map[string][]string, visited []string, repeated string) [][]string {
	current := currentPath[len(currentPath)-1]
	if current == "end" {
		return [][]string{currentPath}
	}
	next, ok := caves[current]
	if !ok {
		return [][]string{}
	}
	res := [][]string{}
	for _, p := range next {
		if contains(visited, p) {
			continue
		}

		nextPath := make([]string, len(currentPath))
		copy(nextPath, currentPath)
		nextPath = append(nextPath, p)

		nextVisited := make([]string, len(visited))
		copy(nextVisited, visited)

		if p != strings.ToUpper(p) {
			if repeated == "" {
				for _, s := range findPathRepeatOnce(nextPath, caves, nextVisited, p) {
					res = appendUnique(res, s)
				}
			}
			nextVisited = append(nextVisited, p)
		}
		for _, s := range findPathRepeatOnce(nextPath, caves, nextVisited, repeated) {
			res = appendUnique(res, s)
		}
	}
	return res
}

func findAllPathsRepeatOnce(caves map[string][]string) int {
	return len(findPathRepeatOnce([]string{"start"}, caves, []string{}, ""))
}

func day12() {
	filename := "input.txt"
	rawLines, err := adventUtils.ReadFileAdvent(filename, 12)
	if err != nil {
		fmt.Errorf("%+v\n", err)
		panic(err)
	}
	caveMap := parseLines(rawLines)

	// Part 1
	paths := findAllPaths(caveMap)
	fmt.Printf("The total number of paths is %d\n", paths)

	// Part 2
	pathsRepeat := findAllPathsRepeatOnce(caveMap)
	fmt.Printf("The total number of paths with one repeat is %d\n", pathsRepeat)

}

func main() {
	adventUtils.Benchmark(day12)
}
