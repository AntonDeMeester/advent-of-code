package main

import (
	"fmt"
	"os"
	"strconv"
	"strings"
)

type command struct {
	direction string
	amount    int
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

func parseLines(lines []string) []command {
	result := []command{}
	for _, line := range lines {
		splitted := strings.Split(line, " ")
		amount, err := strconv.Atoi(splitted[1])
		if err != nil {
			panic(err)
		}
		result = append(result, command{
			direction: splitted[0], amount: amount,
		})
	}
	return result
}

func executeCommandsOne(commands []command) (int, int) {
	depth := 0
	length := 0
	for _, c := range commands {
		if c.direction == "forward" {
			length += c.amount
		} else if c.direction == "down" {
			depth += c.amount
		} else if c.direction == "up" {
			depth -= c.amount
		} else {
			panic(fmt.Sprintf("Unexpected command %s", c.direction))
		}
	}
	return depth, length
}

func executeCommandsTwo(commands []command) (int, int) {
	depth, length, aim := 0, 0, 0
	for _, c := range commands {
		if c.direction == "forward" {
			length += c.amount
			depth += aim * c.amount
		} else if c.direction == "down" {
			aim += c.amount
		} else if c.direction == "up" {
			aim -= c.amount
		} else {
			panic(fmt.Sprintf("Unexpected command %s", c.direction))
		}
	}
	return depth, length
}

func main() {
	filename := "input.txt"
	lines, err := readFile(filename)
	if err != nil {
		lines, err = readFile(fmt.Sprintf("2021/day_2/%s", filename))
		if err != nil {
			panic(err)
		}
	}
	parsedLines := parseLines(lines)
	// depth, length := executeCommandsOne(parsedLines) // Part 1
	depth, length := executeCommandsTwo(parsedLines) // Part 2
	fmt.Printf("We went %dm deep and %dm far, totalling %d", depth, length, depth*length)
}
