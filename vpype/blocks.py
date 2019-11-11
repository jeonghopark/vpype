from typing import Tuple

import click
from shapely import affinity

from .utils import Length
from .vpype import cli, block_processor, BlockProcessor, execute_processors, merge_mls


@cli.command("grid", group="Block processors")
@click.argument("number", nargs=2, default=(2, 2), type=int)
@click.option(
    "-o",
    "--offset",
    nargs=2,
    default=("10mm", "10mm"),
    type=Length(),
    help="Offset between columns and rows. This option understands supported units.",
)
@block_processor
class GridBlockProcessor(BlockProcessor):
    """
    Arrange generated geometries on a NxM grid.

    The number of column and row must always be specified. By default, 10mm offsets are used
    in both directions. Use the `--offset` to override these values.
    """

    def __init__(self, number: Tuple[int, int], offset: Tuple[float, float]):
        self.number = number
        self.offset = offset

    def process(self, processors):
        mls_arr = []
        for i in range(self.number[0]):
            for j in range(self.number[1]):
                mls = execute_processors(processors)
                mls_arr.append(affinity.translate(mls, self.offset[0] * i, self.offset[1] * j))

        return merge_mls(mls_arr)


@cli.command("repeat", group="Block processors")
@click.argument("number", type=int)
@block_processor
class RepeatBlockProcessor(BlockProcessor):
    """
    Stack geometries generated by the block N times on top of each other. N must always be
    provided as argument.
    """

    def __init__(self, number: int):
        self.number = number

    def process(self, processors):
        return merge_mls([execute_processors(processors) for _ in range(self.number)])
