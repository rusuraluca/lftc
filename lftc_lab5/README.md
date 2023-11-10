Class FiniteAutomata will read the file when it is initialized, will parse the input file and then populate all the fields in the class
states = [] -> is an array which contains all the possible states
alphabet = [] -> is an array which contains all the possible letters
initial_state = "" -> a simple string would be enough because we can have only one initial_state
final_states = [] -> the array of final states
transitions = {} -> this would represent a map, where the key represents a pair between (state, alphabet_value) and the value represents the projection of the two
