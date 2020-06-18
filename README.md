# Wound Detection

**_Why_**: wound detection and analysis basically can help aged people evaluate their wound stages before they can have the professional consulting. Meanwhile, wound analysis will be able to play a crucial role in healing when they are at home,Wound assessment is the basis of the wound treatment.

**_How_**: Wound Segmentation and Assessment - area measurement and tissue analysis (location, grade, size, fluid, pain cause of wound) → Wound Classification → Wound status

**_Benefits_**: Helping users to know better about their wounds and helping aged people or their family to better take care of them in wound healing

**Project Documentation**:
https://drive.google.com/drive/folders/1Iwe1mbQ4ZJXRbFFSUbGase7wBOSzbXE9?usp=sharing

**Data Source**: 
_Medetec Wound Database_
http://www.medetec.co.uk/files/medetec-image-databases.html

## Wound Segmentation
Tensorflow DeepLab based semantic segmentation.

### Libraries
Make sure you have followings:
-  Numpy
-  Pillow 1.0
-  tqdm
-  tf Slim (which is included in the "tensorflow/models/research/" checkout)
-  Jupyter notebook
-  Matplotlib
-  Tensorflow

#### Step 1 Environment:
When running locally, the tensorflow/models/research/ directory should be appended to PYTHONPATH. This can be done by running the following from tensorflow/models/research/:
```bash
# From tensorflow/models/research/
export PYTHONPATH=$PYTHONPATH:`pwd`:`pwd`/slim
```
Note: This command needs to run from every new terminal you start. If you wish to avoid running this manually, you can add it as a new line to the end of your ~/.bashrc file.


#### Step 2 :
In order to reduce the number of dimensions of processing DeepLab has to do on each image, we’ll be converting each found RGB color in the segmentation images you made (i.e. RGB(192,128,128)) to an indexed color value (i.e. 1). This will make processing a lot faster.

```bash
python3 convert_rgb_to_index.py
```

Before running, make sure to edit the following:
```python
# palette (color map) describes the (R, G, B): Label pair
palette = {(0,   0,   0) : 0 , #background
           (192,  128, 128) : 1 #wound, you can use your own RGB color
          }
```

#### Step 3:
TensorFlow has a tfrecord format that makes storing training data much more efficient. We’ll need to generate this folder for our dataset. To do so, this repo has made a copy of the build_voc2012_data.py file, which has been saved as a new file (in our case build_pqr_data.py).
```bash
python3 build_pqr_data.py
```

You can edit the build_pqr_data.py file, and make sure there’s a flag for our model’s desired folders.
```python
tf.app.flags.DEFINE_string('image_folder',
                     './PQR/JPEGImages',
                     'Folder containing images.')
tf.app.flags.DEFINE_string(
'semantic_segmentation_folder',
'./PQR/SegmentationClassRaw',
'Folder containing semantic segmentation annotations.')
tf.app.flags.DEFINE_string(
'list_folder',
'./PQR/ImageSets',
'Folder containing lists for training and validation')
tf.app.flags.DEFINE_string(
'output_dir',
'./PQR/tfrecord',
'Path to save converted SSTable of TensorFlow examples.')
```

#### Step 4:
before start training, edit your train-pqr.sh script
```python
# Set up the working environment.
CURRENT_DIR=$(pwd)
WORK_DIR="${CURRENT_DIR}/deeplab"
DATASET_DIR="datasets"
# Set up the working directories.
PQR_FOLDER="PQR"
EXP_FOLDER="exp/train_on_trainval_set"
INIT_FOLDER="${WORK_DIR}/${DATASET_DIR}/${PQR_FOLDER}/${EXP_FOLDER}/init_models"
TRAIN_LOGDIR="${WORK_DIR}/${DATASET_DIR}/${PQR_FOLDER}/${EXP_FOLDER}/train"
DATASET="${WORK_DIR}/${DATASET_DIR}/${PQR_FOLDER}/tfrecord"
mkdir -p "${WORK_DIR}/${DATASET_DIR}/${PQR_FOLDER}/exp"
mkdir -p "${TRAIN_LOGDIR}"
NUM_ITERATIONS=9000
python3 "${WORK_DIR}"/train.py \
--logtostderr \
--train_split="train" \
--model_variant="xception_65" \
--atrous_rates=6 \
--atrous_rates=12 \
--atrous_rates=18 \
--output_stride=16 \
--decoder_output_stride=4 \
--train_crop_size=1000,667 \
--train_batch_size=4 \
--training_number_of_steps="${NUM_ITERATIONS}" \
--fine_tune_batch_norm=true \
--tf_initial_checkpoint="${INIT_FOLDER}/deeplabv3_pascal_train_aug/model.ckpt" \
--train_logdir="${TRAIN_LOGDIR}" \
--dataset_dir="${DATASET}"
```
+ NUM_ITERATIONS: this is how long you want to train for. For me, on a MacBook Pro without GPU support, it took about 12 hours just to run 1000 iterations. You can expect GPU support to speed that up about 10X. At 1000 iterations, I still had a loss of about .17. I would recommend at least 3000 iterations. Some models can be as high as about 20000. You don’t want to overtrain, but you’re better off overtraining than undertraining.
+ train_cropsize: This is the size of the images you’re training on. Your training will go much faster on smaller images. 1000x667 is quite large, and I’d have done better to reduce that size a bit before training. Also, you should make sure these dimensions match in all three scripts: train-pqr,eval-pqr, and vis-pqr.py.

To start training, 
```bash
sh train-pqr.sh
```
which takes a long time...

#### Step 5 Evaluation:
Running ```sh eval-pqr.sh``` from the same directory will calculate the mean intersection over union score for your model. Essentially, this will tell you the number of pixels in common between the actual mask and the prediction of your model.

#### Step 6 Output:
To visualize the actual output of your masks, run ```sh vis-pqr.sh``` from the models/research directory. These will output to your visualization directory you specified.

## Wound Analysis (undergoing...)
SVM 
1. Build the Dataset. We are going to generate a simple data set and then we will read it.
2. Build the DataLoader.
3. Build the model.
4. Define the loss function and the optimizer.
5. Train the model.
