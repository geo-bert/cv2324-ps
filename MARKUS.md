# Report
Für den python code musst du die .sty datei in https://ctan.org/tex-archive/macros/latex/contrib/pythonhighlight?lang=en in den report-latex folder geben

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
- [x] Alle CLI optionen ausschalten mit cifar mean/std -> fertig
- [x] Das beste von den oberen mit den params aus dem paper probieren
- [x] Ohne autoaugment cifar -> läuft muss dann noch das augmentation bild updaten

Muss die Tests rerunnen, keine ahnung welche datei was ist und wo cifar verwendet wurde (wenn nicht angegeben immer example parameter und cifar)
- [x] From Scratch mit Paper Parameters und Imagenet mean/std -> from-scratch-example-parameters_imagenet.txt
- [x] From Scratch mit Example Parameters und Imagenet mean/std -> from-scratch-example-parameters_imagenet.txt
- [x] From Scratch -> from-scratch.txt
- [x] Nur ToTensor() -> only-to-tensor.txt
- [x] Nur ToTensor() aber mit --input_size 32 -> only-totensor_input-is-32
- [x] Normalize mit input size -> normalize_input-is-32.txt
- [x] Auch Resizen -> resize.txt
- [x] CLI optionen auschalten außer AA -> cli-augment-off-but-autoaugment.txt
- [x] CLI optionen ausschalten mit AA

# TODO: mit den parametern aus dem paper trainieren
- [ ] Wie genau funktioniert der Finetune Parameter
- [x] Batchsize bei Finetuning durchprobieren (16, 32, 64, 100) -> fertig
- [x] Ohne CLI Augmentation finetunen -> fertig
- [x] Die beste Konfiguration auf das ganze CIFAR10 finetunen -> fertig

# TODO: Sachen aus dem paper reverten (mit den besten parametern gemacht)
- [ ] Sachen soweit es geht aus paper reverten
- [x] ReLU statt GELU
- [x] BN statt LN -> hab die permutation unter normalisierung geschoben und inplace BatchNorm2d verwendet, statt LayerNorm

# TODO: Bilder Transforms anschauen 
- [x] Wie sehen Bilder nach transform (default und CLI optionen ausschalten) aus?
- [x] Input Size Parameter anschauen -> am ende der forward features wird ein global average pooling gemacht, d.h. input size funktioniert wie es soll d.h. es kommen bilder mit der größe 32 ins netzwerk.

Shapes der Blöcke mit size 32
```
torch.Size([64, 96, 8, 8])
torch.Size([64, 192, 4, 4])
torch.Size([64, 384, 2, 2])
torch.Size([64, 768, 1, 1])
```

Ohne Size
```
torch.Size([64, 96, 56, 56])
torch.Size([64, 192, 28, 28])
torch.Size([64, 384, 14, 14])
torch.Size([64, 768, 7, 7])
```

Am ende kommt immer das raus: `torch.Size([64, 768])`

Transforms wenn alles ausgeschalten ist:
````
RandomResizedCropAndInterpolation(size=(224, 224), scale=(0.08, 1.0), ratio=(0.75, 1.3333), interpolation=PIL.Image.BICUBIC)
RandomHorizontalFlip(p=0.5)
<timm.data.auto_augment.AutoAugment object at 0x7fb517c066e0>
ToTensor()
Normalize(mean=tensor([0.4914, 0.4822, 0.4465]), std=tensor([0.2470, 0.2435, 0.2616]))
````

Transforms wenn alles an ist:
````
RandomResizedCropAndInterpolation(size=(224, 224), scale=(0.08, 1.0), ratio=(0.75, 1.3333), interpolation=PIL.Image.BICUBIC)
RandomHorizontalFlip(p=0.5)
<timm.data.auto_augment.RandAugment object at 0x7f5385f2e3b0>
ToTensor()
Normalize(mean=tensor([0.4914, 0.4822, 0.4465]), std=tensor([0.2470, 0.2435, 0.2616]))
<timm.data.random_erasing.RandomErasing object at 0x7f5385f2de70>
````

Iwie fehlt da color jitter. Im timms wenn autoaugment an ist dann ist automatisch color jitter aus lol.