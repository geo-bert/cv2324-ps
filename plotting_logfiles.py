import sys
import matplotlib.pyplot as plt
import json

import numpy as np

lines = []
labels = []
NR_EPOCHS = int(sys.argv[1])

fig = plt.figure()
ax = plt.subplot()

for color, filename in zip(plt.color_sequences["tab10"],sys.argv[2:]):
    with open(filename, "r") as logfile:
        contents = list(map(lambda x: json.loads(x), logfile.readlines()))
        accuracies = list(map(lambda x: x["test_acc1"], contents))
        epochs = list(map(lambda x: x["epoch"], contents))
        label = filename[len("model_logs/log_"):-len(".txt")]
        max_acc = np.max(accuracies)
        line, = ax.plot(epochs, accuracies, color=color)
        max_line = ax.axhline(y=max_acc, color=color, linestyle=":")
        ax.annotate(f"{max_acc:.2f}%", xy=(NR_EPOCHS, max_acc), color=color, xytext=(0.2*NR_EPOCHS, 0), textcoords="offset points", va="center", size=8)
        lines.append((line, max_line))
        labels.append(label)

box = ax.get_position()
ax.set_position([box.x0, box.y0 + box.height * 0.1,
                 box.width, box.height * 0.9])
ax.legend(lines,labels, bbox_to_anchor=(0., 1.02, 1., .102), loc='lower left',
                      ncols=2, mode="expand", borderaxespad=0.)
ax.set_xticks(range(0, NR_EPOCHS + 1, int(0.1*NR_EPOCHS)))
ax.set_ylabel("Accuracy [%]")
ax.set_xlabel("Epoch")
plt.tight_layout(pad=3)
plt.title("Title", pad=60)
plt.savefig("plots.png", dpi=300)
