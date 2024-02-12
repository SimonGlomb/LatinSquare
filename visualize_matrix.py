import matplotlib.pyplot as plt
import numpy as np

def visualize_matrix(matrix):
    fig, ax = plt.subplots()


    #colors = ["#90EE90"]
    #cmap = plt.matplotlib.colors.ListedColormap(colors)
    #im = ax.imshow(matrix, cmap=cmap)
    im = ax.imshow(matrix, cmap="Blues")

    cbar = ax.figure.colorbar(im, ax=ax)

    ax.set_xticks(np.arange(len(matrix[0])))
    ax.set_yticks(np.arange(len(matrix)))
    ax.set_xticklabels([f"col {i}" for i in range(len(matrix[0]))])
    ax.set_yticklabels([f"row {i}" for i in range(len(matrix))])

    plt.setp(ax.get_xticklabels(), rotation=45, ha="right",
             rotation_mode="anchor")

    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            text = ax.text(j, i, matrix[i][j],
                           ha="center", va="center", color="black")

    ax.set_title("Matrix Visualization")
    fig.tight_layout()
    plt.show()


def visualize_matrix_row_color(matrix, curr_number_of_conflicts_row):

    num_conflicts = 0
    for conflicts in curr_number_of_conflicts_row:
        if conflicts == 0:
            num_conflicts+=1
        
    fig, ax = plt.subplots()

    colors = ["#90EE90"]
    cmap = plt.matplotlib.colors.ListedColormap(colors)
    a = matrix[:num_conflicts].copy()
    im = ax.imshow(a, cmap=cmap)

    ax.set_xticks(np.arange(len(matrix[0])))
    ax.set_yticks(np.arange(len(matrix)))
    ax.set_yticks(ax.get_yticks() + 0.5)
    ax.set_xticklabels([f"col {i}" for i in range(len(matrix[0]))])
    ax.set_yticklabels([f"row {i}" for i in range(len(matrix))])
    
    
    plt.setp(ax.get_xticklabels(), rotation=45, ha="right",
             rotation_mode="anchor")

    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            text = ax.text(j, i, matrix[i][j],
                           ha="center", va="center", color="black")

    ax.set_title("Matrix Visualization")
    fig.tight_layout()
    plt.show()