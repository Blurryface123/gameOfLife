import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# setting up the values for the grid
blackCell = 255
whiteCell = 0
values = [blackCell, whiteCell]



def addGlider(i, j, grid):
    #defining the glider
    glider = np.array([[0, 255, 0],
                       [0, 0, 255],
                       [255, 255, 255]])
    #the 3 define the size of the glider that goes into the grid
    grid[i:i + 3, j:j + 3] = glider

def countNeightbors(grid,x,y,N):
    sum = 0
    for i in range(-1,2):
        for j in range(-1,2):
            #the mod helps take into account the edges
            row = (x + i + N) % N
            col = (y + j + N) % N
            sum += grid[row,col]
    #We extract the center point so we only count the neighbors
    sum -= grid[x,y]
    sum = sum / 255
    return int(sum)


# animation function.  This is called sequentially
def updateAnimation(frameNum, img, grid, N):
    # we copy the grid to create the new grid after checking the neightbors
    newGrid = grid.copy()
    for i in range(N):
        for j in range(N):
            total = countNeightbors(grid,i,j,N)

            # Applying the rules
            if grid[i, j] == blackCell:
                if (total < 2) or (total > 3):
                    newGrid[i, j] = whiteCell
            #dead cell with 3 living neightbors
            else:
                if total == 3:
                    newGrid[i, j] = blackCell

    # the first grid is the one we define and then we modify it
    img.set_data(grid)
    grid[:] = newGrid[:]
    #returns a tuple
    return img,

def main():
    N = 25

    # declare grid
    grid = np.zeros(N*N).reshape(N, N)

    #Here we add the glider, the 13 is the position where the glider starts
    addGlider(13, 13, grid)

    # set up animation
    #https://matplotlib.org/3.2.0/gallery/images_contours_and_fields/interpolation_methods.html
    fig, ax = plt.subplots()
    img = ax.imshow(grid, interpolation='nearest')
    #https://matplotlib.org/3.2.0/api/_as_gen/matplotlib.animation.FuncAnimation.html
    ani = animation.FuncAnimation(fig, updateAnimation,
                                  #Additional arguments to pass to each call to func.
                                  fargs=(img, grid, N,),
                                  interval=1000,
                                  save_count=100)

    plt.show()

if __name__ == '__main__':
    main()