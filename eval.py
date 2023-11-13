from utils import eval_util
import json
import string 
import re

def eval_res():
      L_scores, F_scores = [],[]
      for docId, cand_ans,pred in zip(mydata.raw_test['qID'], mydata.raw_test['answers'], answers):
          print(pred, ' -v.s.- ',str(cand_ans))
          temp_l_scores, temp_f_scores = [],[]
          for ans in cand_ans:
              temp_l_scores.append(eval_util.get_lev_score(ans,pred)) # Levenshein sim
              temp_f_scores.append(eval_util.f1_score(ans, pred)) # f1 score
          L_scores.append(max(temp_l_scores))
          F_scores.append(max(temp_f_scores))
          res.append({"docId":docId, "answer":str(cand_ans), "predict": pred})
      avg_l_score = sum(L_scores) / len(L_scores)
      avg_f_score = sum(F_scores) / len(F_scores)
      print('ANLS:', avg_l_score)
      print('Avg_F1:', avg_f_score)
