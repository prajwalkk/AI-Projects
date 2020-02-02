import constraint
import math
import random
from simanneal import Annealer
import cvxpy as cp
import numpy as np

######################### EXAMPLES OF HOW TO USE PACKAGES ####################

"""" An example of how to set up and solve a CSP for the map of Australia """


def graphColoringExample():
    # First step is to initialize a Problem() from the 'constraint' package.
    colorProblem = constraint.Problem()

    # Next, we will define the values the variables can have, and add them to our problem.
    domains = ["red", "green", "blue"]
    colorProblem.addVariable("WA", domains)  # Ex: "WA" can be "red", "green", or "blue"
    colorProblem.addVariable("NT", domains)
    colorProblem.addVariable("Q", domains)
    colorProblem.addVariable("NSW", domains)
    colorProblem.addVariable("V", domains)
    colorProblem.addVariable("SA", domains)
    colorProblem.addVariable("T", domains)

    # We then add in all of the constraints that must be satisfied.
    # In the map coloring problem we are doing, this means that each section
    # cannot be the same color as any of its neighbors.
    # There are other types of constraints you can add if you want to look at the documentation.
    # However, this type will suffice to do the assignment.
    colorProblem.addConstraint(lambda a, b: a != b, ("WA", "NT"))  # Ex: WA can't be same value (color) as NT
    colorProblem.addConstraint(lambda a, b: a != b, ("WA", "SA"))
    colorProblem.addConstraint(lambda a, b: a != b, ("SA", "NT"))
    colorProblem.addConstraint(lambda a, b: a != b, ("Q", "NT"))
    colorProblem.addConstraint(lambda a, b: a != b, ("SA", "Q"))
    colorProblem.addConstraint(lambda a, b: a != b, ("NSW", "SA"))
    colorProblem.addConstraint(lambda a, b: a != b, ("NSW", "Q"))
    colorProblem.addConstraint(lambda a, b: a != b, ("SA", "V"))
    colorProblem.addConstraint(lambda a, b: a != b, ("NSW", "V"))

    # The constraint problem is now fully defined and we let the solver take over.
    # We call getSolution() and print it.
    print colorProblem.getSolution()


""" Very simple linear program example"""


def convexProgrammingExampleDetailed():
    # This is a trivial convex program to help with using cvxpy
    # We will use a simple least-sqaures problem to demonstrate some of the functionality.
    # These are of the form:

    # Matrices and vectors are represented as numpy arrays. There are several ways to create numpy arrays,
    # Here we will create and fill them directly.
    # First, here is a matrix (numpy array) with one value in it, the number 4
    A = np.array([4])  # Note that np.array() takes a list so the number 4 is in brackets

    # Here is a second matrix with one value in it, the number 1
    b = np.array([1])

    # Define 1 variable to solve for.
    x = cp.Variable(1)

    # We will define the cost that we wish to minimize as the squared value of Ax - b
    # Which in this case is: (4x-1)^2
    cost = cp.sum_squares(A * x - b)

    # Note that this is similar to the above example: cp.norm(x - A[ i,:] ,2)
    # Try it:
    # cost = cp.norm(A*x - b, 2)

    # We use the squared difference here for a few reasons, but for this assignment it is
    # important to remember that the solution works with any constraints you may have set,
    # which in this example none are explicitly set. If we wanted to minimize x for Ax - b without
    # squaring it, the optimal value would be -infinity!
    #   Try for yourself and use this instead:
    #       cost = A*x - b

    # Solution:
    # Because this is set up as solving a single equation, we can do it before hand:
    # From calculus, the minimum is found when the derivative is equal to 0
    # d/dx (4x - 1)^2 = 2(4x-1) = 0
    # 8x - 2 = 0
    # 8x = 2
    # x = 1/4

    prob = cp.Problem(cp.Minimize(cost))
    prob.solve()

    # Print result.
    print 'The optimal value is', prob.value, '(NOTE: this is should be interpreted as being 0)'
    print 'The optimal x is'
    print x.value
    print 'What this says is that for minimizing (4x-1)^2, the optimal value of x is 0.25, which gives the optimal value (4(0.25) - 1)^2 = 0'


""" An example of the syntax to set up and solve a convex problem """
""" Hint: print out various variables below to see what they are/look like and try type()"""


def convexProgrammingExample():
    # Dimensions of matrix A
    n = 2
    m = 10

    # Create matrix A
    A = np.random.randn(m, n)  # Fills matrix with sample(s) drawn from a normal distribution. (will be 0 <= x <= 1)

    # Two variables
    x = cp.Variable(n)

    # Set up what we want to minimize (the sum of squares)
    # Note that the loop is over the total rows (going down the matrix A)
    # Sidenote: think of cp.norm( ,2) as distance (Euclidean)
    #           and think of the whole process as minimizing the total sum of distances
    f = sum([cp.norm(x - A[i, :], 2) for i in range(m)])

    # This is the same as the graphColoring about, but we are combining steps
    # We create a Problem, pass in the objective function and tell cvxpy we want to minimize it
    # And then ask it to solve.
    constraints = [sum(x) == 0]
    result = cp.Problem(cp.Minimize(f), constraints).solve()

    # We want the values of x
    print x.value

    # Try it: What is the optimal value when x is minimize?
    # print result


""" Find an optimal rock paper scissors strategy """
""" Adapted from: https://www2.cs.duke.edu/courses/fall12/cps270/lpandgames.pdf """
""" We will see more about why this works at the end of the course """


def RPS():
    A = np.array([[1, 0, -1, 1], [1, -1, 0, 1], [1, -1, 1, 0], [0, 1, 1, 1], [0, -1, -1, -1]])
    b = np.array([0, 0, 0, 1, -1])
    c = np.array([0, 0, 0, 1])
    x = cp.Variable(4)

    result = cp.Problem(cp.Maximize(x * c),
                        [A * x <= b, x >= 0, x[1] >= 0, x[2] >= 0, x[3] >= 0, x[1] + x[2] + x[3] == 1]).solve()
    print 'Expected Utility: ', x.value[0], ' (Intepret this as zero)'
    print 'Optimal strategy: ', x.value[1], x.value[2], x.value[3], ' (Best to play randomly!)'


""" An example of how to set up and solve an integer problem """
""" Hint: Don't forget to specify integer=True in variable creation"""


def integerProgrammingExample():
    # Create two scalar optimization variables.
    x = cp.Variable(integer=True)
    y = cp.Variable(integer=True)

    # Create two constraints.
    constraints = [x + y == 10,
                   x - y >= 1]

    # Form objective.
    obj = cp.Minimize((x - y) ** 2)

    # Form and solve problem.
    prob = cp.Problem(obj, constraints)
    print prob.solve()


############################ HOMEWORK STARTS HERE #############################

############################## PROBLEM 1 ######################################

""" A helper function to visualize ouput.  You do not need to change this """


def sudokuCSPToGrid(output, psize):
    dim = psize ** 2
    return np.reshape([[output[str(dim * i + j + 1)] for j in range(dim)] for i in range(dim)], (dim, dim))


""" helper function to add variables to the CSP """
""" you do not need to change this"""


def addVar(problem, grid, domains, init):
    numRow = grid.shape[0]
    numCol = grid.shape[1]
    for rowIdx in range(numRow):
        for colIdx in range(numCol):
            if grid[rowIdx, colIdx] in init:
                problem.addVariable(grid[rowIdx, colIdx], [init[grid[rowIdx, colIdx]]])
            else:
                problem.addVariable(grid[rowIdx, colIdx], domains)


""" here you want to add all of the constraints needed.
    # Hint: Use loops!
    #       Remember problem.addConstraint() to add constraints
    #       Some of the constraints you may want can be accessed via constraint.(HereAreSomeBuiltInGeneralConstraints) """


def cstAdd(problem, grid, domains, psize):
    # --------------------
    # Your code
    # print grid, psize
    numCol = grid.shape[0]
    numRow = grid.shape[1]
    # For Row Constraint
    for row in range(numRow):
        rowConstraintMatrix = [grid[row, i] for i in range(numCol)]
        # print rowConstraintMatrix
        problem.addConstraint(constraint.AllDifferentConstraint(), rowConstraintMatrix)
    # For Column Constraints
    for col in range(numCol):
        colConstraintMatrix = [grid[i, col] for i in range(numRow)]
        # print colConstraintMatrix
        problem.addConstraint(constraint.AllDifferentConstraint(), colConstraintMatrix)
    # For Box Constraitns using step feature in range(i,j,step)
    for row in range(0, numRow, psize):
        for col in range(0, numCol, psize):
            boxConstraintMatrix = [grid[i, j] for i in range(row, row + psize) for j in range(col, col + psize)]
            # print boxConstraintMatrix
            problem.addConstraint(constraint.AllDifferentConstraint(), boxConstraintMatrix)
    pass
    # --------------------


""" Implementation for a CSP Sudoku Solver """
""" positions: list of (row,column,value) triples representing the already filled in cells"""
""" psize: the problem size (e.g. 3 for a 3x3 grid of 3x3 squares in a standard Sudoku) """
""" You do not need to change this """


def sudokuCSP(positions, psize):
    sudokuPro = constraint.Problem()
    dim = psize ** 2
    numCol = dim
    numRow = dim
    domains = range(1, dim + 1)
    init = {str(dim * p[0] + p[1] + 1): p[2] for p in positions}
    sudokuList = [str(i) for i in range(1, dim ** 2 + 1)]
    sudoKuGrid = np.reshape(sudokuList, [numRow, numCol])
    addVar(sudokuPro, sudoKuGrid, domains, init)
    cstAdd(sudokuPro, sudoKuGrid, domains, psize)
    return sudokuPro.getSolution()


############################## PROBLEM 2 ######################################

class TravellingSalesmanProblem(Annealer):
    """problem specific data"""
    # latitude and longitude for the twenty largest U.S. cities
    cities = {
        'New York City': (40.72, 74.00),
        'Los Angeles': (34.05, 118.25),
        'Chicago': (41.88, 87.63),
        'Houston': (29.77, 95.38),
        'Phoenix': (33.45, 112.07),
        'Philadelphia': (39.95, 75.17),
        'San Antonio': (29.53, 98.47),
        'Dallas': (32.78, 96.80),
        'San Diego': (32.78, 117.15),
        'San Jose': (37.30, 121.87),
        'Detroit': (42.33, 83.05),
        'San Francisco': (37.78, 122.42),
        'Jacksonville': (30.32, 81.70),
        'Indianapolis': (39.78, 86.15),
        'Austin': (30.27, 97.77),
        'Columbus': (39.98, 82.98),
        'Fort Worth': (32.75, 97.33),
        'Charlotte': (35.23, 80.85),
        'Memphis': (35.12, 89.97),
        'Baltimore': (39.28, 76.62)
    }

    """problem-specific helper function"""
    """you may wish to implement this """

    def distance(self, a, b):
        """Calculates distance between two latitude-longitude coordinates."""
        """ Use self.cities to find a cities coordinates"""
        # -----------------------------
        # Your code
        return math.sqrt(((b[0] - a[0]) ** 2) + ((b[1] - a[1]) ** 2))
        # -----------------------------

    """ make a local change to the solution"""
    """ a natural choice is to swap to cities at random"""
    """ current state is available as self.state """
    """ Note: This is just making the move (change) in the state,
              Worry about whether this is a good idea elsewhere. """
    """ Make sure there is a way for enough of your local changes to
              reach a solution """

    def move(self):
        # --------------------
        # Your code
        a = random.randint(0, len(self.state) - 1)
        b = random.randint(0, len(self.state) - 1)
        self.state[a], self.state[b] = self.state[b], self.state[a]
        pass
        # -------------------------

    """ how good is this state? """
    """ lower is better """
    """ current state is available as self.state """
    """ to get credit your energy must be the total distance travelled in the current state """
    """ Hint: use self.cities and the self.distance function you wrote"""
    """ Hint: e=100 is a random setting, don't read into it being 100 """

    def energy(self):
        # -----------------------
        # Your code
        e = 0.0
        for i in range(len(self.state)):
            e += self.distance(self.cities[self.state[i - 1]], self.cities[self.state[i]])
        return e
        # -----------------------


# Execution part, please don't change it!!!
def annealTSP(initial_state):
    # initial_state is a list of starting cities
    tsp = TravellingSalesmanProblem(initial_state)
    return tsp.anneal()


##########################
# #### PROBLEM 3 ######################################

class SudokuProblem(Annealer):
    """ positions: list of (row,column,value) triples representing the already filled in cells"""
    """ psize: the problem size (e.g. 3 for a 3x3 grid of 3x3 squares in a standard Sudoku) """

    def __init__(self, initial_state, positions, psize):
        self.psize = psize
        self.positions = positions
        super(SudokuProblem, self).__init__(initial_state)

    """ make a local change to the solution"""
    """ current state is available as self.state """
    """ Hint: Remember this is sudoku, just make one local change
              print self.state may help to get started"""
    """ Note that the initial state we give you is purely random
              and may not even respect the filled in squares. """
    """ Make sure there is a way for enough of your local changes to
              reach a solution """

    def move(self):
        # --------------------
        # Your code
        # print self.state
        W = self.psize ** 2
        # print self.positions
        nochange = {(a[0] * W + a[1]): a[2] for a in self.positions}
        for k, v in nochange.items():
            self.state[k] = v
        # print nochange
        array_toChange = [x for x in range(len(self.state)) if x not in nochange.keys()]
        # print array_toChange
        i = random.choice(array_toChange)
        # print i, type(i)
        # if i in nochange:
        #     self.state[i] = nochange[i]
        # else:
        self.state[i] = random.randint(1, self.psize ** 2)
        # print ii,jj
        # self.state[ii], self.state[jj] = self.state[jj], self.state[ii]
        # -------------------------

    """ how good is this state? """
    """ lower is better """
    """ current state is available as self.state """
    """ Hint: How might you 'score' a randomly filled out Sudoku board?
              Loops!
              Python Sets are a quick way to remove duplicates, and then find the total unique elements"""

    def energy(self):
        # -----------------------
        # Your code
        e = 0.0
        uniqueRows = 0
        uniqueCols = 0
        uniqueBoxes = 0
        W = self.psize ** 2
        #Row Constraints
        for row in range(W):
            rowSet = set()
            for col in range(W):
                rowSet.add(self.state[((W) * col) + row])
            uniqueRows -= len(rowSet)
        #Col Constraints
        for col in range(W):
            colSet = set()
            for row in range(W):
                colSet.add(self.state[((W) * col) + row])
            uniqueCols -= len(colSet)
        #Bos Constraints
        for row in range(0, W, self.psize):
            for col in range(0, W, self.psize):
                boxSet = set()
                indices = [i*W+j for i in range(row,row+self.psize) for j in range(col,col+self.psize)]
                for i in indices:
                    boxSet.add(self.state[i])
                uniqueBoxes -= len(boxSet)

        e = (uniqueCols + uniqueRows + uniqueBoxes)
        return e
        # -----------------------


# Execution part, please don't change it!!!
def annealSudoku(positions, psize):
    # initial_state of starting values:
    # it is purely random!
    initial_state = [random.randint(1, psize ** 2) for i in range(psize ** 4)]
    sudoku = SudokuProblem(initial_state, positions, psize)
    sudoku.steps = 100000
    sudoku.Tmax = 100.0
    sudoku.Tmin = 1.0
    return sudoku.anneal()


############################## PROBLEM 4 ######################################

""" Frational Knapsack Problem
    Hint: Think carefully about the range of values your variables can be, and include them in the constraints"""


def fractionalKnapsack(c):
    # --------------------
    # Your code
    A = np.array([5, 3, 1])
    val = np.array([2, 3, 1])

    x = cp.Variable(3)

    constraints = [A * x <= c,
                   x[0] <= 1,
                   x[1] <= 1,
                   x[2] <= 1,
                   x[0] >= 0,
                   x[1] >= 0,
                   x[2] >= 0]

    #Maximising the profit
    final_value = val * x
    knapsack = cp.Problem(cp.Maximize(final_value), constraints)

    return knapsack.solve()


############################## PROBLEM 5 ######################################

""" A helper function to visualize ouput.  You do not need to change this """
""" binary: the output of your solver """
""" psize: the problem size (e.g. 3 for a 3x3 grid of 3x3 squares in a standard Sudoku) """


def sudokuIPToGrid(binary, psize):
    dim = psize ** 2
    x = np.zeros((dim, dim), dtype=int)
    for i in range(dim):
        for j in range(dim):
            for k in range(dim):
                if binary[dim * i + j][k] >= 0.99:
                    x[i][j] = k + 1
    return x


""" Implementation for a IP Sudoku Solver """
""" positions: list of (row,column,value) triples representing the already filled in cells"""
""" psize: the problem size (e.g. 3 for a 3x3 grid of 3x3 squares in a standard Sudoku) """


def sudokuIP(positions, psize):
    # --------------------
    # Your code
    dim = psize ** 2
    M = cp.Variable((dim ** 2, dim), integer=True)  # Sadly we cannot do 3D Variables

    constraints = []
    # ADD YOUR CONSTRAINTS HERE
    for tuple in positions:
        # print str(dim * tuple[0] + tuple[1]) + ":" + str(tuple[2])
        constraints += [M[dim * tuple[0] + tuple[1]][tuple[2] - 1] == 1]

    row_constraint = []

    constraints += [cp.sum(M, axis=0) == dim]
    constraints += [cp.sum(M, axis=1) == 1]
    for i in range(dim ** 2):
        for j in range(dim):
            constraints += [M[i][j] <= 1]
            constraints += [M[i][j] >= 0]

    for i in range(dim):
        for k in range(dim):
            constraints += [cp.sum([M[i * dim + j][k] for j in range(dim)]) == 1]
            constraints += [cp.sum([M[j * dim + i][k] for j in range(dim)]) == 1]


    # for i in range(dim):
    #     for k in range(dim):
    #         row_sum = cp.sum(0)
    #         for j in range(dim):
    #             row_sum+=cp.sum(M[i*dim + j][k])
    #         constraints += row_sum
    # Form objective.
    obj = cp.Minimize(M[0][0])

    # Form and solve problem.
    prob = cp.Problem(obj, constraints)
    prob.solve()
    return M.value
    # --------------------


############################## PROBLEM 6 ######################################

""" Computes MMS allocation """
""" n: number of players """
""" m: number of items """
""" v: matrix of v[i][j] values """
""" MMS: list of MMS[i] for each player i """


def calculateMMSAllocation(n, m, v, MMS):
    # --------------------
    # Your code
    A = cp.Variable((n, m), integer=True)
    constraints = []
    # for i in range(n):
    #     for j in range(m):
    #         constraints += [A[i][j] >= 0]
    #         constraints += [A[i][j] <= 1]
    #
    # for j in range(m):
    #     constraints += [cp.sum(A[i][j]) for i in range(n) == 1]


    return A.value
    # --------------------


""" Computes MMS(i) """
""" n: number of players """
""" m: number of items """
""" v: matrix of v[i][j] values """
""" i: player to compute MMS of """


def calculateMMSValue(n, m, v, i):
    # --------------------
    # Your code
    A = cp.Variable((n, m), integer=True)
    d = cp.Variable()

    return d.value
    # --------------------


######################### TESTING CODE: DEMO THE EXAMPLES OR ADD YOUR OWN TESTS HERE ###############################
# graphColoringExample()
# convexProgrammingExampleDetailed()
# convexProgrammingExample()
# integerProgrammingExample()
# RPS()



