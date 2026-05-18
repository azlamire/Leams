#!/usr/bin/env bats
load 'libs/bats-support/load'
load 'libs/bats-assert/load'

@test "addition using bc" {
  result="$(echo 2+2 | bc)"
  [ "$result" -eq 4 ]
}

@test "addition using dc" {
  result="$(echo 2 2+p | dc)"
  [ "$result" -eq 4 ]
}
