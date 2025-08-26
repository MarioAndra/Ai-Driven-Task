
import re
import random
from difflib import SequenceMatcher

def similarity(a, b):
    return SequenceMatcher(None, str(a).lower(), str(b).lower()).ratio()


def get_task_keywords_from_task_text(task):
    return [word.lower() for word in re.findall(r'\b\w+\b', task) if len(word) > 2]


def tournament_select(scored_list, k=3):
    pick = random.sample(scored_list, min(k, len(scored_list)))
    pick.sort(key=lambda x: x[1], reverse=True)
    return pick[0][0]


def crossover_weights(a, b):
    alpha = random.random()
    return tuple(alpha * a[i] + (1 - alpha) * b[i] for i in range(len(a)))


def mutate_weights(w, mutation_rate):
    new_w = list(w)
    for i in range(len(new_w)):
        if random.random() < mutation_rate:
            new_w[i] = max(0.001, random.gauss(new_w[i], 0.2))
    return tuple(new_w)