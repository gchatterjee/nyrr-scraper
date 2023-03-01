from typing import Dict, List
from race import Race
from update import Addition, Removal, Change, Update


def get_updates(
    old_states: Dict[str, Race], new_states: Dict[str, Race]
) -> List[Update]:
    old_titles = old_states.keys()
    new_titles = new_states.keys()
    addition_titles = new_titles - old_titles
    removal_titles = old_titles - new_titles
    potential_change_titles = old_titles & new_titles
    additions = list(map(lambda title: Addition(new_states[title]), addition_titles))
    removals = list(map(lambda title: Removal(old_states[title]), removal_titles))
    changes = list(
        map(
            lambda title: Change(old_states[title], new_states[title]),
            filter(
                lambda title: old_states[title] != new_states[title],
                potential_change_titles,
            ),
        )
    )
    return additions + removals + changes
