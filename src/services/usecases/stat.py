from src.domain.stats import GroupStats
from src.services.dao.measurements import save_all_groups_stats, get_all_groups_stats
from src.services.stat.pairset import calc_stats
from src.services.usecases.load import get_all_groups


def get_measurements_stats() -> list[GroupStats]:
    _exising_groups = get_all_groups_stats()
    if _exising_groups:
        return _exising_groups

    groups = get_all_groups()
    out: list[GroupStats] = []

    for group in groups:
        out.append(
            GroupStats(
                object=group.object,
                side=group.side,
                stats=calc_stats(group.pairset)
            )
        )

    save_all_groups_stats(out)

    return out
