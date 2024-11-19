import re

class FiniteAutomaton:
    def __init__(self):
        """
        Initializes the finite automaton with empty sets and structures:
        - `states`: The set of all states in the automaton.
        - `alphabet`: The set of valid symbols in the input alphabet.
        - `transitions`: A dictionary that maps a state and symbol to the next state.
        - `start_state`: The initial state of the automaton.
        - `final_states`: A set of states that are considered accepting (or final) states.
        """
        self.states = set()
        self.alphabet = set()
        self.transitions = {}
        self.start_state = None
        self.final_states = set()

    def load_from_file(self, filename):
        """
        Reads the automaton definition from a file and populates the finite automaton.
        The file is expected to have the following format:
        - Line 1: States (e.g., `states: q0,q1,q2`)
        - Line 2: Alphabet symbols (e.g., `alphabet: a,b`)
        - Line 3+: Transitions (e.g., `q0, a -> q1`)
        - A line starting with `start:` specifies the start state.
        - A line starting with `final:` specifies the final states.

        :param filename: Path to the input file containing the automaton definition.
        """
        with open(filename, 'r') as file:
            lines = file.readlines()

        # Parse states (first line)
        self.states = set(state.strip() for state in lines[0].strip().split(":")[1].split(","))
        
        # Parse alphabet (second line)
        self.alphabet = set(symbol.strip() for symbol in lines[1].strip().split(":")[1].split(","))
        
        # Parse transitions, start state, and final states
        for line in lines[2:]:
            if line.startswith("start:"):
                # Parse the start state
                self.start_state = line.strip().split(":")[1].strip()
            elif line.startswith("final:"):
                # Parse final states
                self.final_states = set(state.strip() for state in line.strip().split(":")[1].split(","))
            elif "->" in line:
                # Parse a transition of the form `state, symbol -> next_state`
                match = re.match(r"(\w+),\s*([^\s]+)\s*->\s*(\w+)", line.strip())
                if match:
                    state, symbol, next_state = match.groups()
                    state = state.strip()
                    symbol = symbol.strip()
                    next_state = next_state.strip()
                    if state not in self.transitions:
                        self.transitions[state] = {}
                    self.transitions[state][symbol] = next_state  # Add the transition

    def display(self):
        """
        Displays the finite automaton details:
        - States
        - Alphabet
        - Transitions
        - Start state
        - Final states
        """
        print("States:", self.states)
        print("Alphabet:", self.alphabet)
        print("Transitions:")
        for state, trans in self.transitions.items():
            for symbol, next_state in trans.items():
                print(f"  {state}, {symbol} -> {next_state}")
        print("Start State:", self.start_state)
        print("Final States:", self.final_states)

    def is_valid_token(self, token):
        """
        Checks if a given string (token) is accepted by the finite automaton.
        The string is processed character by character to follow the defined transitions.

        :param token: The input string to validate.
        :return: True if the token is valid (ends in a final state), False otherwise.
        """
        current_state = self.start_state  # Start at the initial state
        for char in token:
            # Check if the character is in the alphabet and if there is a valid transition
            if char not in self.alphabet or current_state not in self.transitions or char not in self.transitions[current_state]:
                print(f"Character {char} not in alphabet or no valid transition.")
                return False  # Invalid character or transition
            next_state = self.transitions[current_state][char]  # Follow the transition
            print(f"Transitioning from {current_state} with {char} to {next_state}")
            current_state = next_state  # Update the current state
        
        # Check if the final state is an accepting state
        return current_state in self.final_states

# Main Program
if __name__ == "__main__":
    # Create a finite automaton instance
    fa = FiniteAutomaton()
    
    # Load the automaton definition from a file
    fa.load_from_file("FA.in")
    
    # Display the automaton's details
    fa.display()

    # Prompt the user to test strings
    print("\nEnter strings to check if they are valid tokens (type 'exit' to quit):")
    while True:
        test_string = input("> ").strip()  # Read user input
        if test_string.lower() == "exit":  # Exit condition
            print("Exiting...")
            break
        if fa.is_valid_token(test_string):  # Validate the token
            print(f"The string '{test_string}' is a valid token.")
        else:
            print(f"The string '{test_string}' is NOT a valid token.")
