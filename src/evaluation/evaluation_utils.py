from sklearn.metrics import precision_score, recall_score, f1_score
from difflib import SequenceMatcher
import json

def normalize_string(s):
    return s.lower().strip() if s else ""

def compare_strings(pred, true):
    return normalize_string(pred) == normalize_string(true)

def compare_lists(pred_list, true_list):
    pred_set = set(map(normalize_string, pred_list))
    true_set = set(map(normalize_string, true_list))
    tp = len(pred_set & true_set)
    precision = tp / len(pred_set) if pred_set else 0
    recall = tp / len(true_set) if true_set else 0
    f1 = 2 * precision * recall / (precision + recall) if precision + recall else 0
    return precision, recall, f1

def compare_dict_lists(pred_list, true_list, keys):
    matched_pred = set()
    matched_true = set()
    
    for i, true_item in enumerate(true_list):
        for j, pred_item in enumerate(pred_list):
            if j in matched_pred:
                continue
            match = all(compare_strings(pred_item.get(k, ""), true_item.get(k, "")) for k in keys)
            if match:
                matched_true.add(i)
                matched_pred.add(j)
                break

    tp = len(matched_true)
    precision = tp / len(pred_list) if pred_list else 0
    recall = tp / len(true_list) if true_list else 0
    f1 = 2 * precision * recall / (precision + recall) if precision + recall else 0
    return precision, recall, f1

def evaluate(pred, true):
    results = {}
    results["name"] = compare_strings(pred["name"], true["name"])
    results["email"] = compare_strings(pred["email"], true["email"])
    results["phone"] = compare_strings(pred["phone"], true["phone"])
    
    skills_p, skills_r, skills_f1 = compare_lists(pred["skills"], true["skills"])
    results["skills"] = {"precision": skills_p, "recall": skills_r, "f1": skills_f1}

    edu_p, edu_r, edu_f1 = compare_dict_lists(pred["education"], true["education"], keys=["degree", "field", "institution", "year"])
    results["education"] = {"precision": edu_p, "recall": edu_r, "f1": edu_f1}

    exp_p, exp_r, exp_f1 = compare_dict_lists(pred["experience"], true["experience"], keys=["title", "company", "duration"])
    results["experience"] = {"precision": exp_p, "recall": exp_r, "f1": exp_f1}

    return results
