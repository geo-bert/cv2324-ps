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
- Die standard Learning Rate war beim Finetuning mega schlecht ~10%.

# TODO: wiederholen von data augmentation runs
- [x] Was ist der Testing Transform? (Centercrop or not) -> `--input_size 32 und --crop_pct 1` dann accuracy goes stonks
- [x] Gar keine Transforms (nur ToTensor()) -> in Dataloader transform mit `transforms.ToTensor()` ersetzen
- [x] Normalisieren mit imagenet mean/std -> in create_transform `return transforms.Compose([transforms.ToTensor(), transforms.Normalize(mean,std)])` statt transform
- [x] Normalisieren mit cifar mean/std -> in create_transform `mean = (0.49139968, 0.48215827, 0.44653124), std = (0.24703233, 0.24348505, 0.26158768)` [reference](https://stackoverflow.com/questions/66678052/how-to-calculate-the-mean-and-the-std-of-cifar10-data)
- [x] Normalize + Bilder groß machen -> im compose noch `(args.input_size, args.input_size), interpolation=transforms.InterpolationMode.BICUBIC`
- [x] Gleiche mit cifar normalize -> fertig
- [ ] Alle CLI optionen ausschalten mit imagenet mean/std 
- [x] Alle CLI optionen ausschalten mit cifar mean/std -> fertig
- [ ] Einzelne CLI optionen manuell hinzufügen
- [x] Das beste von den oberen mit den params aus dem paper probieren

# TODO: mit den parametern aus dem paper trainieren
- [ ] Wie genau funktioniert der Finetune Parameter
- [ ] Beide Arten von Finetuning
- [ ] Die andere Art von From Scratch (aber nur 100 Epochen)
- [ ] Andere Modelle für das Finetuning ausprobieren
- [x] Batchsize bei Finetuning durchprobieren (16, 32, 64, 100) -> fertig
- [x] Ohne CLI Augmentation finetunen -> fertig
- [ ] Mit dem --model Parameter herumspielen
- [ ] Die beste Konfiguration auf das ganze CIFAR10 finetunen -> läuft

# TODO: Sachen aus dem paper reverten
- [ ] Sachen soweit es geht aus paper reverten
- [x] ReLU statt GELU
- [x] BN statt LN -> hab die permutation unter normalisierung geschoben und inplace BatchNorm2d verwendet, statt LayerNorm
- [ ] Schauen, ob man ein originales ConvNet hernehmen kann
- [ ] Bester Revert mit bester Data Augmentation und Hyperparametern kombinieren

# TODO Marcel: 
- [ ] Wie sehen Bilder nach transform (default und CLI optionen ausschalten) aus?