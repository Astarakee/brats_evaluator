from auxiliary.nifti.io import read_nifti

from panoptica import (
    InputType,
    Panoptica_Evaluator,
    Panoptica_Aggregator,
    ConnectedComponentsInstanceApproximator,
    NaiveThresholdMatching,
)
from panoptica.utils.segmentation_class import SegmentationClassGroups
from panoptica.utils.label_group import LabelMergeGroup

from auxiliary.turbopath.turbopath import turbopath

from concurrent.futures import ProcessPoolExecutor, as_completed

import os


from tqdm import tqdm


import pandas as pd

import tempfile


def analyze_exam(
    prediction_path: str,
    label_path: str,
    identifier: str,
    panoptica_config_path: str,
) -> dict:
    """
    Evaluate a single exam using Panoptica.

    Args:
        prediction_path (str): _description_
        label_path (str): _description_
        identifier (str): _description_
        panoptica_config_path (str): _description_

    Returns:
        dict: _description_

        Note: The function returns a dictionary containing the evaluation results.
        Note this is very ugly as the evaluator is instantiated again and again for every exam and panoptica's batch processing capabilities (Aggregator) are not used.
        This should be improved in the future.
    """

    # file io

    ref_masks = read_nifti(label_path)
    ref_masks = ref_masks.astype(int)

    pred_masks = read_nifti(prediction_path)
    pred_masks = pred_masks.astype(int)

    evaluator = Panoptica_Evaluator.load_from_config(panoptica_config_path)

    # call evaluate
    group2result = evaluator.evaluate(
        prediction_arr=pred_masks,
        reference_arr=ref_masks,
        # subject_name=identifier,
    )

    # convert to dict and add identifier
    results = {k: r.to_dict() for k, r in group2result.items()}
    results["subject_name"] = identifier

    return results


# if __name__ == "__main__":
#     results = analyze_exam(
#         prediction_path="./sample_data/preds/BraTS-MET-01352-000.nii.gz",
#         label_path="./sample_data/reference/BraTS-MET-01352-000.nii.gz",
#         identifier="BraTS-MET-01352-000.nii.gz",
#         panoptica_config_path= "./brats-configs/config_mets.yaml",
#     )
#
#     print(results)
