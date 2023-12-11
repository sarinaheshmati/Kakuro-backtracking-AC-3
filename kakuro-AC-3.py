from itertools import permutations
import time

#The AC-3 algorithm returns false if the domain becomes empty of some variable
def AC_3(csp, queue=None):
    if queue == None:
        queue = [(xi,xj) for xi in csp.variables for xj in csp.neighbours[xi]]
    while queue:
        xi,xj = queue.pop(0)
        removed = csp.remove_inconsistent_values(xi, xj)
        if removed:
            if len(csp.domain[xi]) == 0:
                return False
            #add the neighbour arcs in queue if some value is removed
            for neighbour in csp.neighbours[xi]:
                queue.append((neighbour, xi))
    return True
                
#recursive backtracking algorithm which returns the solution if it exists
def recursive_backtracking(csp,assignment):
    if len(assignment) == len(csp.variables):
        return assignment
    variable = csp.select_unassigned_variable(assignment)
    for value in csp.domain_values(variable):
        if csp.is_consistent(variable, value, assignment):
            assignment[variable] = value
            result = recursive_backtracking(csp,assignment)
            if result != None:
                return result
    if variable in assignment:
        del assignment[variable]
    return None

def backtracking_search(csp):
    return recursive_backtracking(csp,{})

#makes the csp problem from the given table   
def make_csp(number_rows,number_columns,horizontal,vertical):
    variables = []
    domain = {}
    constraints = {}
    neighbours = {}
    
    #For the horizontal
    for i in range(number_rows):
        for j in range(number_columns):
            #Find the clues
            if horizontal[i][j] != "#" and horizontal[i][j] != "0":
                u_variable_name = "YR" + str(i) + "," + str(j)
                #Add the newly found variable to the list
                variables.append(u_variable_name)
                neighbours[u_variable_name] = []
                k = j + 1
                counter = 0
                #set the domain, constraints, neighbours and variables of the position
                while k < number_columns:
                    if horizontal[i][k] == "0":
                        x_variable_name = "X" + str(i) + "," + str(k)
                        variables.append(x_variable_name)
                        neighbours[x_variable_name] = []
                        neighbours[x_variable_name].append(u_variable_name)
                        neighbours[u_variable_name].append(x_variable_name)
                        domain[x_variable_name] = [l for l in range(1,min(int(horizontal[i][j]),10))]
                        constraints[u_variable_name+x_variable_name] = counter
                        counter += 1
                    else:
                        break
                    k += 1
                domain[u_variable_name] = [p for p in permutations([1,2,3,4,5,6,7,8,9],k-j-1) if sum(p) == int(horizontal[i][j])]
                j = k

    #For the vertical
    for j in range(number_columns):
        for i in range(number_rows):
            #find the clues
            if vertical[i][j] != "#" and vertical[i][j] != "0":
                u_variable_name = "YD"+str(i)+","+str(j)
                #Add the variable
                variables.append(u_variable_name)
                neighbours[u_variable_name] = []
                k = i + 1
                counter = 0
                #set the domains constraints neighbours variables in block
                while k < number_rows:
                    if vertical[k][j] == "0":
                        x_variable_name = "X"+str(k)+","+str(j)
                        if x_variable_name not in variables:
                            variables.append(x_variable_name)
                        if x_variable_name in neighbours:
                            neighbours[x_variable_name].append(u_variable_name)
                        else:
                            neighbours[x_variable_name] = [u_variable_name]
                        neighbours[u_variable_name].append(x_variable_name)
                        if x_variable_name in domain:
                            domain[x_variable_name] = list(set(domain[x_variable_name]).intersection(set([l for l in range(1,min(int(vertical[i][j]),10))])))
                        else:
                            domain[x_variable_name] = [l for l in range(1,min(int(vertical[i][j]),10))]
                        constraints[u_variable_name+x_variable_name] = counter
                        counter += 1
                    else:
                        break
                    k += 1
                domain[u_variable_name] = [p for p in permutations([1,2,3,4,5,6,7,8,9],k-i-1) if sum(p) == int(vertical[i][j])]
                i = k
    #return the csp
    return KakuroCSP(variables, domain, neighbours, constraints)

#class to define the csp
class KakuroCSP:
    def __init__(self, variables, domain, neighbours, constraints):
        self.variables = variables
        self.domain = domain
        self.neighbours = neighbours
        self.constraints = constraints
        
    #returns the domain values of a variable
    def domain_values(self, variable):
        return self.domain[variable]
 
    #if assigning the value to the variable is consistent with previous assignments the method returns True, if not, returns False
    def is_consistent(self, variable, value, assignment):
    #checking if the variable is a blank position or one assigned with clues
        if variable[0] == "Y":
            for neighbour in self.neighbours[variable]:
                if neighbour in assignment:
                    if assignment[neighbour] != value[self.constraints[variable+neighbour]]:
                        return False
            return True
        else:
            for neighbour in self.neighbours[variable]:
                if neighbour in assignment:
                    if assignment[neighbour][self.constraints[neighbour+variable]] != value:
                        return False
            return True

    #removes the inconsistent values from the domain hence, prunes the domain
    #returns true if a value is removed
    def remove_inconsistent_values(self, xi, xj):
        removed = False
        for valueXi in self.domain[xi]:
            remove = True
            for valueXj in self.domain[xj]:
                if xj[0] == "Y":
                    if valueXi == valueXj[self.constraints[xj+xi]]:
                        remove = False
                        break
                else:
                    if valueXi[self.constraints[xi+xj]] == valueXj:
                        remove = False
                        break
            if remove:
                self.domain[xi].remove(valueXi)
                removed = True
        return removed

    #finds a variable which is not assigned and returns it
    def select_unassigned_variable(self, assignment):
        for variable in self.variables:
            if variable not in assignment:
                return variable

def main():
#choose an input (a game board)

    # #input 1 (5*6):
    # horizontal = [['#', '#', '#', '#', '#', '#'], ['4', '0', '0', '#', '#', '#'],
    #              ['10', '0', '0', '0', '0', '#'], ['#', '10', '0', '0', '0', '0'],
    #               ['#', '#', '#', '3', '0', '0']]
    # vertical = [['#', '3', '6', '#', '#', '#'], ['#', '0', '0', '7', '8', '#'], 
    #             ['#', '0', '0', '0', '0', '3'], ['#', '#', '0', '0', '0', '0'], 
    #             ['#', '#', '#', '#', '0', '0']]
    # number_rows = 5
    # number_columns = 6

    # #input 2 (8*8):
    # horizontal = [['#', '#', '#', '#', '#', '#', '#', '#'], ['16', '0', '0', '#', '24', '0', '0', '0'],
    #             ['17', '0', '0', '29', '0', '0', '0', '0'], ['35', '0', '0', '0', '0', '0', '#', '#'],
    #             ['#', '7', '0', '0', '8', '0', '0', '#'], ['#', '#', '16', '0', '0', '0', '0', '0'], 
    #             ['21', '0', '0', '0', '0', '5', '0', '0'], ['6', '0', '0', '0', '#', '3', '0', '0']]
    # vertical = [['#', '23', '30', '#', '#', '27', '12', '16'], ['#', '0', '0', '#', '17', '0', '0', '0'],
    #             ['#', '0', '0', '15', '0', '0', '0', '0'], ['#', '0', '0', '0', '0', '0', '12', '#'],
    #             ['#', '#', '0', '0', '7', '0', '0', '7'], ['#', '11', '10', '0', '0', '0', '0', '0'], 
    #             ['#', '0', '0', '0', '0', '#', '0', '0'], ['#', '0', '0', '0', '#', '#', '0', '0']]
    # number_rows = 8
    # number_columns = 8

    #input 3 (10*10):
    horizontal = [['#', '#', '#', '#', '#', '#', '#', '#', '#', '#'], ['4', '0', '0', '#', '#', '#', '#', '16', '0', '0'],
                ['23', '0', '0', '0', '#', '#', '24', '0', '0', '0'], ['#', '13', '0', '0', '0', '23', '0', '0', '0', '#'],
                ['#', '#', '#', '11', '0', '0', '0', '0', '#', '#'], ['#', '#', '#', '23', '0', '0', '0', '#', '#', '#'], 
                ['#', '#', '25', '0', '0', '0', '0', '#', '#', '#'], ['#', '8', '0', '0', '0', '7', '0', '0', '0', '#'], 
                ['6', '0', '0', '0', '#', '#', '6', '0', '0', '0'], ['3', '0', '0', '#', '#', '#', '#', '4', '0', '0']]

    vertical = [['#', '10', '10', '#', '#', '#', '#', '#', '23', '16'], ['#', '0', '0', '17', '#', '#', '#', '17', '0', '0'],
                ['#', '0', '0', '0', '20', '#', '30', '0', '0', '0'], ['#', '#', '0', '0', '0', '20', '0', '0', '0', '#'],
                ['#', '#', '#', '#', '0', '0', '0', '0', '#', '#'], ['#', '#', '#', '6', '0', '0', '0', '#', '#', '#'], 
                ['#', '#', '7', '0', '0', '0', '0', '3', '9', '#'], ['#', '4', '0', '0', '0', '#', '0', '0', '0', '4'], 
                ['#', '0', '0', '0', '#', '#', '#', '0', '0', '0'], ['#', '0', '0', '#', '#', '#', '#', '#', '0', '0']]
    number_rows = 10
    number_columns = 10

#Find the solution by making the csp problem and doing the backtracking search
    t1 = time.time()
    csp = make_csp(number_rows,number_columns,horizontal,vertical)
    #apply arc consistency on all arcs
    AC_3(csp)
    assignment = backtracking_search(csp)
    t2 = time.time()
    t3 = t2 - t1
    if assignment == None:
        print("input's dimensions: ", number_rows, "*", number_columns)
        print("solving time with improved backtracking (by arc-conistancy): ", t3)
        print("No solution")
    else:
        print("input's dimensions: ", number_rows, "*", number_columns)
        print("time: ", t3)
        print("the answer is: ")
        print("solved Horizontal: ")
        for i in range(number_rows):
            for j in range(number_columns):
                if horizontal[i][j] == '#' or horizontal[i][j] != '0':
                    print(horizontal[i][j], end=" ")
                else:
                    print(str(assignment["X"+str(i)+","+str(j)]), end=" ")
            print()
        print("solved Vertical: ")
        for i in range(number_rows):
            for j in range(number_columns):
                if horizontal[i][j] == '#' or horizontal[i][j] != '0':
                    print(vertical[i][j], end=" ")
                else:
                    print(str(assignment["X"+str(i)+","+str(j)]), end=" ")
            print()
        
if __name__ == "__main__":
   main()
