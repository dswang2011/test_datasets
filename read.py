import pickle

# file = open('vqa_devtest_prompts.pkl','rb')
# data = pickle.load(file)

# print(data.keys())
# # dict_keys(['docvqa', 'visualmrc', 'wtq', 'websrc', 'buddie'])
# baselines:
# 1) websrc (Mathieu); 2) DocVQA + VisualMRC (Simerjot); 3) WTQ + Buddie (Yulong) => GPT4
# 4) all 5 datasets (Donghsheng) => Llama-7B-instruct (and Mistral-7B)
# 

# print(data['wtq'])

# print(data['wtq'].keys())
# # Index(['task', 'dataset', 'split', 'id', 'docId', 'prompt', 'answers', 'type', 'page', 'tokens', 'bboxes'],


def get_ds(ds_name):
    file = open('vqa_devtest_prompts.pkl','rb')
    data = pickle.load(file)
    ds = data[ds_name]
    return ds
    
    # prompts = ds['prompt']
    # docs = [' '.join(tokens) for tokens in ds['tokens']]
    # answers = ds['answers']
    # return prompts, answers, docs

if __name__=='__main__':
    ps, ans, ds = get_ds('wtq')
    cnt = 0
    for p,a,d in zip(ps,ans,ds):
        print(p, a)
        print(d)    # seems the first 10 doc are the same??
        print('---')

        cnt+=1
        if cnt>10: break

