import matplotlib.pyplot as plt

data = [
    [16, 8, 19, 8, 21],
    [63, 12, 36, 20, 46],
    [79, 16, 75, 19, 101]
    ]

plt.boxplot(data)

plt.xticks([1, 2, 3], ['A*', 'Dijkstra', 'Greedy'])

# plt.show()
fig = plt.gcf()
plt.savefig('miau',
            #bbox='tight',
            edgecolor=fig.get_edgecolor(),
            facecolor=fig.get_facecolor(),
            dpi=150
            )