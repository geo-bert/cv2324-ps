# Aufsetzen

mit `pip install -r requirements.txt` die requirements installieren
ich hab es im WSL in einem venv gemacht, wenn der sich bei dir über CUDA oder so aufregt hab ich das gemacht bei mir: [link](https://github.com/microsoft/WSL/issues/5663#issuecomment-1068499676)

das sind die ganzen args die ich fürs finetuning jetzt verwendet habe:
`--model convnext_tiny
--epochs 10
--data_set CIFAR
--data_path dataset
--finetune https://dl.fbaipublicfiles.com/convnext/convnext_tiny_1k_224_ema.pth
--downsample 10
--warmup_epochs 0
--num_workers 8
--output_dir
network
--cutmix 0
--mixup 0
--lr 4e-4`

Ich hab es bei mir durchlaufen lassen, ergebnisse kannst du im [logfile_finetune.log](logfile_finetune.log) sehen. Hat Max accuracy: 95.80%
und Training time 0:23:41

Was ich geändert habe am code, kannst du eh im Git log anschauen.

# Observationen (für den report dann)
* Die standard Learning Rate war beim Finetuning mega schlecht ~10%.

# TODO: wiederholen von data augmentation runs
* Gar keine Transforms (nur ToTensor())
* Normalisieren mit imagenet mean/std
* Normalisieren mit cifar mean/std
* Alle CLI optionen ausschalten mit imagenet mean/std
* Alle CLI optionen ausschalten mit cifar mean/std
* Einzelne CLI optionen manuell hinzufügen
* Das beste von den oberen mit den params aus dem paper probieren

# TODO: mit den parametern aus dem paper trainieren
* Beide Arten von Finetuning
* Die andere Art von From Scratch (aber nur Epochen)
* Andere Modelle für das Finetuning ausprobieren
* Batchsize bei Finetuning durchprobieren (16, 32, 64, 100)
* Mit dem --model Parameter herumspielen
* Die beste Konfiguration auf das ganze CIFAR10 finetunen

# TODO: Sachen aus dem paper reverten
* Sachen soweit es geht aus paper reverten
* Schauen, ob man ein originales ConvNet hernehmen kann
* Bester Revert mit bester Data Augmentation und Hyperparametern kombinieren