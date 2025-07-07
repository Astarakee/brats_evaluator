# BraTS Evaluation Pipline

This repository is inspired by [Panoptica evaliation pipeline](https://github.com/BrainLesion/panoptica) 
to compute the segmentation metrics for [BraTS 2025 challenges](https://www.synapse.org/Synapse:syn64153130/wiki/630130).

- Panoptica is a comprehensive package with three main modules: Instance Approximator, Instance Matcher,
and Instance Evaluator. 
This repository is inspired by the [Panoptica evaluation pipeline](https://github.com/neuronflow/brats_modality_ablation_nnUnet/blob/main/panoptica_evaluation.py).

- The evaluation pipeline computes the standard segmentation metrics both on subject-wise and lesion-wise levels.
- BraTS 2025 cluster of challenges includes 7 segmentation tasks.
While this pipeline can be employed for quantification of all 7 tasks, it is used only for the [Brain Metastais segmentation task](https://www.synapse.org/Synapse:syn64153130/wiki/631058) in BraTS 2025 challenges.


## Installation

`Panoptica` is the main requirement for this pipeline.
With a Python 3.10+ environment, you can install it from [pypi.org](https://pypi.org/project/panoptica/)
```
pip install panoptica
```
followed by cloning the repo:
```
git clone https://github.com/Astarakee/brats_evaluator.git

cd /path/to/brats_evaluator
```

or alternatively:
```
git clone https://github.com/Astarakee/brats_evaluator.git

cd /path/to/brats_evaluator

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