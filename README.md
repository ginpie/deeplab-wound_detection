# Wound Detection

Data Source: Medetec Wound Database
http://www.medetec.co.uk/files/medetec-image-databases.html

## Wound Segmentation
CNN

* Step 1:
```bash
# From tensorflow/models/research/
export PYTHONPATH=$PYTHONPATH:`pwd`:`pwd`/slim
```
* Step 2:
```bash
python3 convert_rgb_to_index.py
```
* Step 3:
```bash
python3 build_pqr_data.py
```
* Step 4:
```bash
sh train-pqr.sh
```


## Wound Analysis
SVM
1. Build the Dataset. We are going to generate a simple data set and then we will read it.
2. Build the DataLoader.
3. Build the model.
4. Define the loss function and the optimizer.
5. Train the model.
