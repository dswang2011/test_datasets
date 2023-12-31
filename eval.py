import json
import string 
import re
import Levenshtein as lev
from collections import Counter
from typing import Sequence
from pycocoevalcap.tokenizer.ptbtokenizer import PTBTokenizer
from pycocoevalcap.cider.cider import Cider


def normalize_answer(s):
    """Lower text and remove punctuation, articles and extra whitespace."""
    def remove_articles(text):
        return re.sub(r"\b(a|an|the)\b", " ", text)
    def white_space_fix(text):
        return " ".join(text.split())
    def remove_punc(text):
        exclude = set(string.punctuation)
        return "".join(ch for ch in text if ch not in exclude)
    def lower(text):
        return text.lower()
    return white_space_fix(remove_articles(remove_punc(lower(s))))


def f1_score(ground_truth, prediction):
    prediction_tokens = normalize_answer(prediction).split()
    ground_truth_tokens = normalize_answer(ground_truth).split()
    common = Counter(prediction_tokens) & Counter(ground_truth_tokens)
    num_same = sum(common.values())
    if num_same == 0:
        return 0
    precision = 1.0 * num_same / len(prediction_tokens)
    recall = 1.0 * num_same / len(ground_truth_tokens)
    f1 = (2 * precision * recall) / (precision + recall)
    return f1


def cider(
    targets: Sequence[Sequence[str]],
    predictions: Sequence[str]) -> float:
    """Compute CIDEr score."""
    coco_tokenizer = PTBTokenizer()
    scorer = Cider()
    score, scores = scorer.compute_score(
      gts=coco_tokenizer.tokenize({
          str(i): [{"caption": t} for t in target]
          for i, target in enumerate(targets)
      }),
      res=coco_tokenizer.tokenize({
          str(i): [{"caption": prediction}]
          for i, prediction in enumerate(predictions)
      }))
    score = float(score) * 100.0
    scores = [float(s) * 100.0 for s in scores.tolist()]
    return score, scores


def get_lev_score(ans, pred):
    return lev.ratio(ans.lower(),pred.lower()) # Levenshein sim


def eval_res(answers, predictions):
    '''
    answers: list of answers of list
    predictions: list of predictions 
    '''
    L_scores, F_scores = [],[]
    for cand_ans,pred in zip(answers, predictions):
        print(pred, ' -v.s.- ',str(cand_ans))
        temp_l_scores, temp_f_scores = [],[]
        for ans in cand_ans:
            temp_l_scores.append(get_lev_score(ans,pred)) # Levenshein sim
            temp_f_scores.append(f1_score(ans, pred)) # f1 score
            L_scores.append(max(temp_l_scores))
            F_scores.append(max(temp_f_scores))
        avg_l_score = sum(L_scores) / len(L_scores)
        avg_f_score = sum(F_scores) / len(F_scores)
    print('ANLS:', avg_l_score)
    print('Avg_F1:', avg_f_score)
    return avg_l_score, avg_f_score


if __name__=='__main__':
    dataset_name = "docvqa"
    output_json = 'final_{dataset_name}.json' # param1
    with open(output_json) as fw:
        results = json.load(fw)
    # ensemble
    answers, predictions = [], []
    for item in results:
        answers.append(item['gold'])
        predictions.append(item['answer'])
    lev_score, f_score = eval_res(answers,predictions)
    print('lev_score:', lev_score)
    print('f_score:', f_score)


      
