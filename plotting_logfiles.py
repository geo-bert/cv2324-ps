import sys
import matplotlib.pyplot as plt
import json

import numpy as np

lines = []
labels = []
NR_EPOCHS = int(sys.argv[1])
FILENAME = sys.argv[2]

fig = plt.figure()
ax = plt.subplot()

for color, filename in zip(plt.color_sequences["tab10"], sys.argv[3:]):
    with open(filename, "r") as logfile:
        contents = list(map(lambda x: json.loads(x), logfile.readlines()))
        accuracies = list(map(lambda x: x["test_acc1"], contents))
        epochs = list(map(lambda x: x["epoch"], contents))
        label = filename[len("model_logs/data_augmentation/log_"):-len(".txt")]
        last_acc = accuracies[-1]
        line, = ax.plot(epochs, accuracies, color=color)
        length = len(accuracies)
        supporting_line_range = np.arange(length - 1, np.ceil(NR_EPOCHS * 1.1))
        max_line, = ax.plot(supporting_line_range, np.repeat(last_acc, len(supporting_line_range)), linestyle=":")
        ax.annotate(f"{last_acc:.2f}%", xy=(NR_EPOCHS-0.5, last_acc), color=color, xytext=(NR_EPOCHS*0.2, 0),
                    textcoords="offset points", va="center", size=8, annotation_clip=False)
        lines.append((line, max_line))
        labels.append(label)

box = ax.get_position()
ax.set_position([box.x0, box.y0 + box.height * 0.1,
                 box.width, box.height * 0.9])
ax.legend(lines, labels, bbox_to_anchor=(0., 1.02, 1., .102), loc='lower left',
          ncols=2, mode="expand", borderaxespad=0.)
ax.set_xticks(range(0, NR_EPOCHS + 1, int(0.1 * NR_EPOCHS)))
ax.set_xlim([-0.05*(NR_EPOCHS-1), (NR_EPOCHS-1)*1.05])
ax.set_ylabel("Accuracy [%]")
ax.set_xlabel("Epoch")
plt.tight_layout(pad=3)
plt.title(FILENAME.split("/")[-1].replace("_", " ")[:-4].title(), pad=15 + 15 * np.ceil(len(lines) / 2))
plt.savefig(FILENAME, dpi=300)
