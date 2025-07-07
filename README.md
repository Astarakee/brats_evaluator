# BraTS Evaluation Pipline

This repository is inspired by [Panoptica evaliation pipeline](https://github.com/BrainLesion/panoptica) 
and [GANDLF](https://github.com/mlcommons/GaNDLF) to compute the segmentation evaluation metrics for [BraTS 2025 challenges](https://www.synapse.org/Synapse:syn64153130/wiki/630130).

- GANDLF (Generally Nuanced Deep Learning Framework) is an open-source deep learning framework specifically designed for
medical imaging. Its primary goal is to lower the barrier to entry for developing, training, and deploying robust deep
learning models for tasks like segmentation, classification, and regression in medical images.
- Panoptica is a comprehensive package with three main modules: Instance Approximator, Instance Matcher,
and Instance Evaluator. This repository is inspired by the [evaluation pipeline](https://github.com/neuronflow/brats_modality_ablation_nnUnet/blob/main/panoptica_evaluation.py).

- The evaluation pipeline computes the standard segmentation metrics both on subject-wise and lesion-wise levels.
- BraTS 2025 cluster of challenges includ[analyze_brats.py](analyze_brats.py)es 7 segmentation tasks. While this pipeline can be employed for 
quantification of all 7 tasks, for 2025 challenge it is used only for the [Brain Metastais segmentation task](https://www.synapse.org/Synapse:syn64153130/wiki/631058).


## Installation

With a Python 3.10+ environment, you can install panoptica from [pypi.org](https://pypi.org/project/panoptica/)
```
pip install panoptica
```
or alternatively:
```
git clone NAME

cd /path/to/NAME

pip install -r requirements.txt
```

## Usage
A minimal example of using this pipeline to compute the segmentation metrics can be:

```python
from analyze_brats import analyze_exam

path_ref_mask = "./sample_data/reference/BraTS-MET-01352-000.nii.gz"
path_pred_mask = "./sample_data/preds/BraTS-MET-01352-000.nii.gz"
path_config = "./brats-configs/config_mets.yaml"
subject_identifier = path_ref_mask.split("/")[-1]

results = analyze_exam(
    prediction_path=path_pred_mask,
    label_path=path_ref_mask,
    identifier=subject_identifier,
    panoptica_config_path=path_config,
)
```
It shoule be noted that predicted segmentation mask should have identical image spacing meta-data
(such as orientation, voxel-spacing, and image origin) as reference mask.

The quantified metrics will be stored in `results` as a dictionary. Depending on the `config` file it can have
different metrics. For the provided Brain Metastasis example, the following metrics are calculated:
```
"num_ref_instances": XX,
"num_pred_instances": XX,
"tp": XX,
"fp": XX,
"fn": XX,
"prec": XX,
"rec": XX,
"rq": XX,
"sq_dsc": XX,
"sq_dsc_std": XX,
"pq_dsc": XX,
"sq_hd95": XX,
"sq_hd95_std": XX,
"sq_nsd": XX,
"sq_nsd_std": XX,
"global_bin_dsc": XX,
"global_bin_hd95": XX,
"global_bin_nsd": XX
```
from which global_bin_dsc, global_bin_hd95, global_bin_nsd, prec, recl represent the subject-wise metrics and
the rest are the calculated lesion-wise metrics.

Finally, note that the above-mentioned metrics are caclulated for the defined regions in the `config` file.
For Brain Metastasis, these regions include:
```
et: enhancing tissue
netc: non-enhancing tumor core
rc: resection cavity
tc: tumor core
wt: whole tumor
```
## Reference
For further details about the evaluation pipeline, we refer you the official [Panoptica package](https://github.com/BrainLesion/panoptica).