# PDA Simulator
Simulates a Push-Down Automata with strings.

## Requirements
* Python 3.5 or above

## How to run the simulation
* In the root directory of the project, run: `python3 main.py`

## Menu Actions
* After starting the program, a user interface will display 5 options:
    1. Loop through strings in JSON file
    2. Enter in string manually
    3. Print PDA transition table
    4. Move to next file in `./files/` directory.
    5. Exit the program

## Adding Custom PDA files
* All PDA files are located under `./files/`
* Must be `.json` files

## Custom PDA file format
* Lambda (λ) must be represented as `E`
* If lambda transitions are used, `E` needs to be added to the alphabet list.
* Transitions are of the format: `["start state", "character to transition on", "state to transition to", "left PDA stack character", "right PDA stack character"]`
* Example: `["q1", "a", "q2", "E", "E"]`
* Example Explanation: The state `q1` when fed the character `a` will transition to `q2` and will pop lambda from the stack
* NOTE: If a state does not have any transitions leaving itself or going into itself, leave it blank under the `transitions` list in the file.

## Printing Computation of PDA to Console
* Under the PDA file, add the value `show_computation`
* With a value of `1`, it will print the PDA's computation
* `0` will only print whether the string was accepted or rejected by the PDA

## Unit Tests
* In the root directory of the project, run: `python3 -m unittest`
* Location of unit tests: `./tests/`
