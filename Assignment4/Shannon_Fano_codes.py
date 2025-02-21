from math import log2, ceil

def compute_probability(word:str) -> dict[str:int]:
    return {letter: word.count(letter)/len(word) for letter in set(word)}

def compute_sizes(prob_dist:dict[str:int]) -> dict[str:list[int,int]]:
    sorted_items = sorted(prob_dist.items(), key=lambda x: x[1], reverse=True)
    return {letter: [prob, ceil(log2(1/prob))] for letter, prob in sorted_items}

def shannon_fano_codification(word:str):
    prob_dist = compute_probability(word)
    sizes = compute_sizes(word)

    Bsf_code = {list(sizes.keys())[0]:sizes[list(sizes.keys())[1]]*0}

    for i in range(1,len(list(sizes.keys()))):
        continue
    pass