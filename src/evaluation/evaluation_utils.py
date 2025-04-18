def normalize_string(s):
    if isinstance(s, str):
        return s.lower().strip() if s else ""

def compare_simple_field(gt, pred):
    gt_norm = normalize_string(gt)
    pred_norm = normalize_string(pred)
    return int(gt_norm == pred_norm), int(gt_norm != pred_norm), int(pred_norm != gt_norm)

def compare_list_of_strings(gt_list, pred_list):
    gt_set = set(normalize_string(item) for item in gt_list)
    pred_set = set(normalize_string(item) for item in pred_list)
    tp = len(gt_set & pred_set)
    fn = len(gt_set - pred_set)
    fp = len(pred_set - gt_set)
    return tp, fn, fp

def compare_list_of_objects(gt_list, pred_list):
    matched_pred_indices = set()
    tp = 0
    for gt_obj in gt_list:
        match_found = False
        for idx, pred_obj in enumerate(pred_list):
            if idx in matched_pred_indices:
                continue
            if all(normalize_string(gt_obj.get(k, '')) == normalize_string(pred_obj.get(k, '')) for k in gt_obj):
                match_found = True
                matched_pred_indices.add(idx)
                break
        if match_found:
            tp += 1
    fn = len(gt_list) - tp
    fp = len(pred_list) - tp
    return tp, fn, fp

def evaluate_extraction(gt, pred):
    total_tp = total_fn = total_fp = 0

    # Simple fields
    for field in ["name", "email", "phone"]:
        tp, fn, fp = compare_simple_field(gt[field], pred[field])
        total_tp += tp
        total_fn += fn
        total_fp += fp

    # List of strings
    tp, fn, fp = compare_list_of_strings(gt["skills"], pred["skills"])
    total_tp += tp
    total_fn += fn
    total_fp += fp

    # List of objects
    for field in ["education", "experience"]:
        tp, fn, fp = compare_list_of_objects(gt[field], pred[field])
        total_tp += tp
        total_fn += fn
        total_fp += fp

    precision = total_tp / (total_tp + total_fp) if (total_tp + total_fp) > 0 else 0
    recall = total_tp / (total_tp + total_fn) if (total_tp + total_fn) > 0 else 0
    f1 = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0

    return {
        "true_positives": total_tp,
        "false_negatives": total_fn,
        "false_positives": total_fp,
        "precision": round(precision, 4),
        "recall": round(recall, 4),
        "f1_score": round(f1, 4)
    }