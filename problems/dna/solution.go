package main

import (
	"bufio"
	"fmt"
	"os"
)

func solve(s string) string {
	var a, c, g, t int

	for _, nucleotide := range s {
		switch nucleotide {
		case 'A':
			a++
		case 'C':
			c++
		case 'G':
			g++
		case 'T':
			t++
		}
	}

	return fmt.Sprintf("%d %d %d %d", a, c, g, t)
}

func main() {
	s := bufio.NewScanner(os.Stdin)
	if !s.Scan() {
		fmt.Fprintln(os.Stderr, "Error reading input:", s.Err())
		os.Exit(1)
	}

	fmt.Println(solve(s.Text()))
}
