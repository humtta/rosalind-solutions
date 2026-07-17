package main

import (
	"bufio"
	"fmt"
	"os"
)

func solve(s string) string {
	nucleotides := []rune(s)

	for i := range nucleotides {
		if nucleotides[i] == 'T' {
			nucleotides[i] = 'U'
		}
	}

	return string(nucleotides)
}

func main() {
	s := bufio.NewScanner(os.Stdin)
	if !s.Scan() {
		fmt.Fprintln(os.Stderr, "Error reading input:", s.Err())
		os.Exit(1)
	}

	fmt.Println(solve(s.Text()))
}
