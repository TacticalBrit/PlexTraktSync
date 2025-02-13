from functools import cached_property


class RichProgressBar:
    def __init__(self, iterable, total, options=None, desc=""):
        self.iter = iter(iterable)
        self.options = options or {}
        self.desc = desc
        self.total = total
        self.i = 0

    def __iter__(self):
        return self

    def __next__(self):
        res = self.iter.__next__()
        self.update()
        return res

    def __enter__(self):
        self.progress.__enter__()
        return self

    def __exit__(self, *exc):
        self.progress.__exit__(*exc)

    def update(self):
        self.i += 1
        self.progress.update(self.task_id, completed=self.i)

    @cached_property
    def task_id(self):
        return self.progress.add_task(self.desc, total=self.total)

    @cached_property
    def progress(self):
        from tqdm.rich import FractionColumn, RateColumn

        from rich.progress import (BarColumn, Progress, TimeElapsedColumn,
                                   TimeRemainingColumn)

        args = (
            "[progress.description]{task.description}"
            "[progress.percentage]{task.percentage:>4.0f}%",
            BarColumn(bar_width=None),
            FractionColumn(
                unit_scale=False,
                unit_divisor=1000,
            ),
            "[",
            TimeElapsedColumn(),
            "<",
            TimeRemainingColumn(),
            ",",
            RateColumn(
                unit="it",
                unit_scale=False,
                unit_divisor=1000,
            ),
            "]"
        )
        progress = Progress(*args, **self.options)

        return progress
