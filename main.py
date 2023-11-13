import read
import time
import json
import GPT4_api_template as gpt_api

if __name__=='__main__':
    # 'docvqa', 'visualmrc', 'wtq', 'websrc', 'buddie'
    dataset_name = 'docvqa' # param1: dataset name
    final_json_output = 'final_.json'   # param2: output path

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
        item = str({"questionId":qID, "answer":pred_answer})

        if cnt == 0:
            print(doc)
            print(question)
            print(pred_answer)
            print(answers)
            print(item)

        with open('temp_.txt', "a") as fw:
            fw.write(item + '\n')
        cnt+=1
        if cnt%50==0: 
            print('-sleep-')
            time.sleep(5)
            with open('temp_.json', "w") as fw:
                json.dump(res, fw)

    # res = json.dumps(res)
    # with open('gpt_res.json','a') as fw:
    #     fw.write(str(res))
    with open(final_json_output, "w") as fw:
        json.dump(res, fw)
