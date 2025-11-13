# README

A **Python** program to print the route between two employees in an organisation chart that has been read in from a file.


The program creates a tree of Employees and then traverses it to find the route. In doing so we use the Least Common Ancestor (LCA), that is by going up in the hierarchy from the two employees the first manager they have in common.

## Running the program

An example run:
```
python challenge.py superheroes.txt "Batman" "Super Ted"
```

## Running the tests

The tests are contained in tests.py and can be run with:

```
python tests.py
```

## Code flow

The code flow for challenge.py:

```
run_program
	read_file_into_dict
	create_tree
	find_shortest_route
		compare_names
		id_occurrences
			compare_names
		employee_depth
		find_lca_route
```

## Assumptions

- Employee id is unique
- If we specify the same name twice at the command line we expect there to be two employees and not just print a route to the same person
- Taking "There may be gaps in the sequence (where people have left the company)." to mean gaps in Employee IDs and not disconnected charts

On the directional arrows:
- If we can just go from employee 1 to employee 2 (or vice-versa) without a common manager then we just have a -> from whichever is the lowest in the hierarchy to whichever is the highest. If we actually intended direction of travel then lines 185-186 will need un-commenting and tests changing for this.
- If we need to use a common manager then a -> means going up the hierarchy from employee 1 to the common manager and a <- means going up from from employee 2 to the common manager. 