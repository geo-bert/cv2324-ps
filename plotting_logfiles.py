import sys
import matplotlib.pyplot as plt
import json

for filename in sys.argv[1:]:
    with open(filename, "r") as logfile:
        contents = list(map(lambda x: json.loads(x), logfile.readlines()))
        accuracies = list(map(lambda x: x["test_acc1"], contents))
        epochs = list(map(lambda x: x["epoch"], contents))
        label = filename[len("model_logs/log_"):-len(".txt")]
        plt.plot(epochs, accuracies, label=label)

plt.legend()
plt.xticks(range(0, 101, 5))
plt.ylabel("Accuracy [%]")
plt.xlabel("Epoch")
plt.savefig("plots.png", dpi=300)
