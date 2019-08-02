#!/usr/bin/env bash

curl -v -H "Content-Type: application/json" --data "@./payload.json" http://localhost:8081/evaluate_board_state
