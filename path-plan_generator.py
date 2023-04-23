n = int(input('Enter size of maze \n'))
no = int(input('Enter number of obstacles \n'))

print('Enter obstacles one by one. each obstacle coordinates should be separated by space')
# obstacles = {(2, 2), (3, 3), (3, 4), (4, 1)}
obstacles = set()
for i in range(0,n):
    obstacles.add(tuple(int(x) for x in input().split()))

# start = (1, 1)
start = tuple(int(x) for x in input('enter start state separated by space \n').split())
# goal = (4, 4)
goal = tuple(int(x) for x in input('enter goal state separated by space \n').split())

def generate_smtlib(file):
    file.write("(set-logic QF_BV) \n\n")

    # Boolean variables for each cell and time step
    file.write(";Boolean variables for each cell and time step \n")
    for t in range(n*n):
        for x in range(1, n + 1):
            for y in range(1, n + 1):
                file.write(f"(declare-fun c_{x}_{y}_{t} () Bool) \n")
    file.write("\n")

    # Initial position
    file.write(";Initial position \n")
    file.write(f"(assert c_{start[0]}_{start[1]}_0) \n")
    file.write("\n")

    # Goal positions
    file.write(";Goal positions \n")
    file.write(f"(assert (or \n")
    for t in range(n*n):
        file.write(f"  c_{goal[0]}_{goal[1]}_{t} \n")
    file.write(")) \n")
    file.write("\n")

    # Obstacles
    file.write(";Obstacle variables \n")
    for t in range(n*n):
        for x, y in obstacles:
            file.write(f"(assert (not c_{x}_{y}_{t})) \n")
    file.write("\n")

    # Preconditions
    file.write(";Precondition variables \n")
    for t in range(n*n):
        for x1 in range(1, n + 1):
            for y1 in range(1, n + 1):
                for x2 in range(1, n + 1):
                    for y2 in range(1, n + 1):
                        if (x1, y1) != (x2, y2):
                            file.write(f"(assert (=> c_{x1}_{y1}_{t} (not c_{x2}_{y2}_{t}))) \n")
    file.write("\n")

    # Actions
    file.write(";Action variables \n")
    for t in range(n*n - 1):
        for x in range(1, n + 1):
            for y in range(1, n + 1):
                file.write("(assert (=> \n")
                file.write(f"  c_{x}_{y}_{t} \n")
                file.write("  (or \n")
                if x > 1:
                    file.write(f"    c_{x-1}_{y}_{t+1} \n")
                if x < n:
                    file.write(f"    c_{x+1}_{y}_{t+1} \n")
                if y > 1:
                    file.write(f"    c_{x}_{y-1}_{t+1} \n")
                if y < n:
                    file.write(f"    c_{x}_{y+1}_{t+1} \n")
                file.write("  ) \n")
                file.write(")) \n")
    file.write("\n")

    file.write("(check-sat) \n")
    file.write("(get-model) \n")

with open('path-plan.smtlib2', 'w') as output_file:
    generate_smtlib(output_file)
