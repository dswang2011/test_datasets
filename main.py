import read
import eval
import tqdm

if __name__=='__main__':
    # 'docvqa', 'visualmrc', 'wtq', 'websrc', 'buddie'
    mydata = read.get_ds('docvqa')  # split = test only 
    print(mydata.keys())
    # 'task', 'dataset', 'split', 'id', 'docId', 'prompt', 'answers', 'type', 'page', 'tokens', 'bboxes'

    cnt = 0
    res = []
    offset = 1000
    for i,inst in enumerate(mydata.iloc[offset:].iterrows()):
        print(inst)
        words = inst.tokens
        question = inst.prompt
        qID = [inst.docId, inst.id]

        answers = inst.answers

        doc = ' '.join(words)

        answer = get_completion(doc,question)
        if not answer: continue

        answer = answer.split("Answer:")[1].strip() 
        # deliver to GPT
        res.append({"id":i+offset, "questionId":qID, "answer":answer})
        item = str({"questionId":qID, "answer":answer})

        if cnt == 0:
            print(doc)
            print(question)
            print(answer)
            print(answers)
            print(item)

        with open('temp4.txt', "a") as fw:
            fw.write(item + '\n')
        cnt+=1
        if cnt%50==0: 
            print('-sleep-')
            time.sleep(5)
            with open('temp4.json', "w") as fw:
                json.dump(res, fw)

    # res = json.dumps(res)
    # with open('gpt_res.json','a') as fw:
    #     fw.write(str(res))
    with open('final_.json', "w") as fw:
        json.dump(res, fw)
