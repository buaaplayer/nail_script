import warnings

import cv2
import numpy as np

from post_processing import transform_preds

def _calc_distances(preds, targets, mask, normalize):
    """Calculate the normalized distances between preds and target.
    Note:
        batch_size: N
        num_keypoints: K
        dimension of keypoints: D (normally, D=2 or D=3)
    Args:
        preds (np.ndarray[N, K, D]): Predicted keypoint location.
        targets (np.ndarray[N, K, D]): Groundtruth keypoint location.
        mask (np.ndarray[N, K]): Visibility of the target. False for invisible
            joints, and True for visible. Invisible joints will be ignored for
            accuracy calculation.
        normalize (np.ndarray[N, D]): Typical value is heatmap_size
    Returns:
        np.ndarray[K, N]: The normalized distances.
          If target keypoints are missing, the distance is -1.
    """
    N, K, _ = preds.shape
    distances = np.full((N, K), -1, dtype=np.float32)
    # handle invalid values
    normalize[np.where(normalize <= 0)] = 1e6
    distances[mask] = np.linalg.norm(((preds - targets) / normalize[:, None, :])[mask], axis=-1)
    return distances.T

def keypoint_epe(pred, gt, mask):
    """Calculate the end-point error.
    Note:
        batch_size: N
        num_keypoints: K
    Args:
        pred (np.ndarray[N, K, 2]): Predicted keypoint location.
        gt (np.ndarray[N, K, 2]): Groundtruth keypoint location.
        mask (np.ndarray[N, K]): Visibility of the target. False for invisible
            joints, and True for visible. Invisible joints will be ignored for
            accuracy calculation.
    Returns:
        float: Average end-point error.
    """

    distances = _calc_distances(
        pred, gt, mask,
        np.ones((pred.shape[0], pred.shape[2]), dtype=np.float32))
    distance_valid = distances[distances != -1]
    return distance_valid.sum() / max(1, len(distance_valid))