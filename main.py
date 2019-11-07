import os
import argparse
import sys

from enum import Enum

class ConflictType(Enum):
    MERGE = "merge"

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", type=str, 
                        help="path to resovle git conflict",
                        required=True)
    parser.add_argument("-c", type=str,
                         help="type of git conflict.\nTypes: 1. merge",
                          required=True)
    args = vars(parser.parse_args(sys.argv[1:]))
    path = args["p"]
    conflict = args["c"]
    if str(conflict).upper() == ConflictType.MERGE.name:
        import merge_conflict_resolver
        merge_conflict_resolver.resolve(path)
    else:
        print("ERROR: No such type of conflict")
    pass