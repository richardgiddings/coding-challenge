from argparse import ArgumentParser
import sys


"""
    A class representing an Employee
"""
class Employee:

    # initialise employee
    def __init__(self, employee_id, name, manager_id):
        self.employee_id = employee_id
        self.employee_name = name
        self.manager_id = manager_id
        self.reports = []
        self.manager = None

    # add a report to this employee
    def add_report(self, employee):
        self.reports.append(employee)

    def __str__(self):
        return f'employee_id={self.employee_id}, employee_name={self.employee_name}, manager_id={self.manager_id}, reports={self.reports}'


"""
    Purpose:
        Compare two names for equality

    Arguments:
        name_one - first name to compare
        name_two - second name to compare

    Returns:
        True if names match, False otherwise
"""
def compare_names(name_one: str, name_two: str):

    if ' '.join(name_one.lower().split()) == ' '.join(name_two.lower().split()):
        return True
    return False


"""
    Purpose:
        Get the depth of an Employee in the tree

    Arguemnts:
        node           - the root of the tree
        target_name    - the employee we want the depth of
        depth:         - the current depth
        found          - a list containing depth of employee and its Employee object
        other_employee - don't want to find the same employee twice when traversing
                         if there are two employees with the same name

    Returns:
        None (note that 'found' returned by reference)
"""
def employee_depth(node: Employee, target_name: str, depth: int, found: list, other_employee: Employee):

    if node is None:
        return
    if compare_names(node.employee_name, target_name):
        if other_employee is None or node.employee_id != other_employee.employee_id:
            found[0] = depth
            found[1] = node
    for employee in node.reports:
        if found[0] == 0:
            employee_depth(employee, target_name, depth+1, found, other_employee)


"""
    Purpose:
        Taking the command line arguments read the file
        into a dictionary of Employee objects
    
    Arguments:
        filename - the input file

    Returns:
        A dictionary containing Employee objects keyed by employee_id
"""
def read_file_into_dict(filename: str):

    try:
        employee_dict = {}
        with open(filename, 'r') as f:
            next(f) # skip the header
            for line in f:
                columns = [x.strip() for x in line[1:].split('|')]
                employee = Employee(columns[0], columns[1], columns[2])
                employee_dict[columns[0]] = employee

        return employee_dict

    except FileNotFoundError:
        print(f'The file {filename} does not exist.')
    except Exception as e:
        print(e)
    
    sys.exit(1)


"""
    Purpose:
        Create the tree from the employee details we added to
        the dictionary employee_dict
    
    Argmements:
        employee_dict - dictionary of employee objects

    Returns:
        The root of the tree created
"""
def create_tree(employee_dict: dict):

    for employee_id in employee_dict:
        employee = employee_dict[employee_id]
        manager_id = employee.manager_id
        if manager_id == '':
            root = employee
        else:
            manager = employee_dict[manager_id]
            if manager is not None: # maybe they have no manager?
                employee_dict[manager_id].add_report(employee)
                employee.manager = manager

    return root


"""
    Purpose:
        Find the route using the Least Common Ancestor, i.e. the first
        manager in common traversing the tree upwards

    Arguments:
        lowest_node         - the employee lowest in hierarchy by depth
        lowest_node_depth   - the depth of the lowest employee
        highest_node        - the employee hieghest in hierarchy by depth
        highest_node_depth  - the depth of the highest employee
        route_end_node      - the employee we are finding a path to

    Returns:
        A list containing the route between the two employees
"""
def find_lca_route(
        lowest_node: Employee, lowest_node_depth: int, 
        highest_node: Employee, highest_node_depth: int, 
        route_end_node: Employee
    ):

    # get to same depth as the highest node on the lowest node side
    difference = lowest_node_depth - highest_node_depth
    count = 0
    current_1 = lowest_node
    route_1 = [f'{current_1.employee_name} ({current_1.employee_id})']
    while count != difference:
        current_1 = current_1.manager
        route_1.append(f'{current_1.employee_name} ({current_1.employee_id})')
        count += 1

    # we are at the same level searching up the tree so if the employees are the
    # same then we don't have to go down at all to find the route
    if current_1.employee_id == highest_node.employee_id:
        if route_1[0] == f'{route_end_node.employee_name} ({route_end_node.employee_id})':
            route_1.reverse()
        return route_1

    # find the route on both sides to LCA by repeatedly moving one level up
    current_2 = highest_node
    route_2 = [f'{current_2.employee_name} ({current_2.employee_id})']
    if current_1.manager.employee_id == current_2.manager.employee_id:
        route_1.append(f'{current_1.manager.employee_name} ({current_1.manager.employee_id})')
    else:
        current_1 = current_1.manager
        current_2 = current_2.manager
        while current_1 is not None:

            if current_1.employee_id == current_2.employee_id:
                route_1.append(f'{current_1.employee_name} ({current_1.employee_id})')
                break
            else:
                route_1.append(f'{current_1.employee_name} ({current_1.employee_id})')
                route_2.append(f'{current_2.employee_name} ({current_2.employee_id})')

            current_1 = current_1.manager
            current_2 = current_2.manager

    # concatenate routes and reverse the end part of route
    if route_1:
        if route_1[0] == f'{route_end_node.employee_name} ({route_end_node.employee_id})':
            route_1.reverse()
            route = route_2 + route_1
        else:
            route_2.reverse()
            route = route_1 + route_2
        return route

    return []


"""
    Purpose:
        Get the shortest route between two employees

    Arguments: 
        root            - the root of the tree
        employee_name_1 - route from this employee
        employee_name_2 - to this employee

    Returns:
        The chain of employees from employee_name_1 to employee_name_2
        as a string
"""
def find_shortest_route(root: Employee, employee_name_1: str, employee_name_2: str):

    # find the depth of each employee
    found = [0, None]
    employee_depth(root, employee_name_1, 1, found, None)
    employee_1_depth, employee_1 = found
    if found[0] == 0:
        return f'"{employee_name_1}" is not an employee'
    
    found = [0, None] 
    employee_depth(root, employee_name_2, 1, found, employee_1)
    employee_2_depth, employee_2 = found
    if found[0] == 0:
        return f'"{employee_name_2}" is not an employee or there is only one with this name'

    # now get the route
    if employee_2_depth > employee_1_depth:
        route = find_lca_route(employee_2, employee_2_depth, employee_1, employee_1_depth, employee_2)
    elif employee_2_depth < employee_1_depth:
        route = find_lca_route(employee_1, employee_1_depth, employee_2, employee_2_depth, employee_2)
    else:
        route = find_lca_route(employee_1, employee_1_depth, employee_2, employee_2_depth, employee_2)
    
    if route:
        return ' -> '.join(route)

    return "No route"


"""
    Purpose: 
        Run the program to get the shortest chain between two employees
    
    Arguments:
        filename        - the filename containing the organisation chart
        employee_1_name - the name of the start employee 
        employee_2_name - the name of the end employee

    Returns:
        A string containing the chain between the two employees if
        there is one
"""
def run_program(filename: str, employee_1_name: str, employee_2_name: str):

    # 1. Go through the file and add an Employee for each employee to a dictionary -> O(n) time
    employee_dict = read_file_into_dict(filename)

    # 2. Run through the Employees and use manager_id to add children -> O(n) time
    root = create_tree(employee_dict)

    # 3) Find the shortest route between two employees
    chain = find_shortest_route(root, employee_1_name, employee_2_name)
    
    return chain


if __name__ == '__main__':

    parser = ArgumentParser()
    parser.add_argument('filename')
    parser.add_argument('employee_name_1')
    parser.add_argument('employee_name_2')
    args = parser.parse_args()

    chain = run_program(args.filename, args.employee_name_1, args.employee_name_2)
    print(chain)