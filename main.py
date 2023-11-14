import read
import time
import json
import GPT4_api_template as gpt_api

if __name__=='__main__':
    # 'docvqa', 'visualmrc', 'wtq', 'websrc', 'buddie'
    dataset_name = 'docvqa' # param1: dataset name
    final_json_output = f'final_{dataset_name}.json'   # param2: output path

    mydata = read.get_ds(dataset_name)  # split = test only 
    print(mydata.keys())
    # 'task', 'dataset', 'split', 'id', 'docId', 'prompt', 'answers', 'type', 'page', 'tokens', 'bboxes'

    cnt = 0
    res = []
    offset = 0
    for i,inst in mydata.iloc[offset:].iterrows():
    # for i, inst in mydata.iterrows():
        words = inst.tokens
        question = inst.prompt
        qID = [inst.docId, inst.id]
        # 1) doc ID
        if dataset_name == 'docvqa':
            qID = inst.id[2]
        # 2) answers
        answers = inst.answers
        # 3) doc text
        doc = ' '.join(words)
        # 
        pred_answer = gpt_api.get_completion(doc,question)
        if not pred_answer: continue

        if "Answer:" in pred_answer:
            pred_answer = pred_answer.split("Answer:")[1].strip()
        
        # deliver to GPT
        res.append({"id":i+offset, "questionId":qID, "answer":pred_answer, "gold":answers})

        if cnt == 0:
            print(doc)
            print(question)
            print(pred_answer)
            print(answers)

        cnt+=1
        if cnt%50==0: 
            with open(final_json_output, "w") as fw:
                json.dump(res, fw)

    with open(final_json_output, "w") as fw:
        json.dump(res, fw)
