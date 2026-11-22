"""Inspectable lexical query hints; these are not generated evidence or answers."""

import re

from .index import tokenize


RANKING_VERSION = "context-v1"
SETTINGS = {"expansion_weight": 0.5, "page_weight": 0.7,
            "title_hint_boost": 0.4, "one_result_per_page": True}
# Small development glossary. Trigger whole phrases, expand once, preserve every
# original query term. No question IDs, source IDs, expected pages or answers.
CONCEPTS = [
    (["life support", "eclss"], ["eclss", "life", "support"]),
    (["lightest", "lighter"], ["mass", "minimize", "minimizing", "minimum"]),
    (["weightlessness", "weightless"], ["microgravity"]),
    (["stay fit", "fitness"], ["exercise", "countermeasures", "deconditioning", "rehabilitation"]),
    (["injured", "illness", "sick"], ["medical", "injury"]),
    (["brought back", "bring back"], ["return", "evacuation"]),
    (["ordinary day", "typical day", "daily life"], ["daily", "workday", "schedule", "personal"]),
    (["duties", "free time"], ["workload", "personal", "utilization"]),
    (["prepositioned", "prepositioning"], ["predeploy", "predeployed", "deployment"]),
    (["thousand"], ["1000", "1", "000"]),
]
TITLE_HINTS = frozenset(["eclss", "medical", "radiation", "operations"])


def query_weights(question):
    normalized = " " + " ".join(re.findall(r"[a-z0-9]+", question.casefold())) + " "
    weights = {term: 1.0 for term in tokenize(question)}
    for triggers, terms in CONCEPTS:
        if any(" " + phrase + " " in normalized for phrase in triggers):
            for term in terms:
                weights.setdefault(term, SETTINGS["expansion_weight"])
    return weights
