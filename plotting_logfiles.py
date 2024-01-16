import sys
import matplotlib.pyplot as plt

for filename in sys.argv[1:]:
    with open(filename, "r") as logfile:
        accuracies = filter(lambda x: x.startswith("Accuracy of the model"), logfile.readlines())
        accuracies = list(map(lambda x: float(x.split(" ")[-1][:-3])/100, accuracies))
        epochs = range(0, len(accuracies))
        plt.plot(epochs, accuracies, label=filename)

plt.legend()
plt.tight_layout()
plt.xticks(range(0, 101, 5))
plt.savefig("plots.png", dpi=300)
