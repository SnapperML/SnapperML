# TODO: Add support to load/save from/to S3
# TODO: Add connection to models part

import uproot
import glob
from functools import reduce


def get_tree_keys(tree):
    keys = tree.keys()
    if keys:
        children_keys = {key: get_tree_keys(tree[key]) for key in keys}
        if not any(children_keys.values()):
            return list(children_keys.keys())
        else:
            return children_keys
    else:
        return {}


def get_file_metadata(root_directory):
    all_trees = dict(root_directory.allitems(filterclass=lambda cls: issubclass(cls, uproot.tree.TTreeMethods)))
    return {k: get_tree_keys(v) for k, v in all_trees.items()}


def find_branches_by_string(tree, branches):
    branches = branches.strip()
    if b"*" in branches or b"?" in branches or b"[" in branches:
        for name in tree.iterkeys(recursive=True):
            if name == branches or branches == b'*' or glob.fnmatch.fnmatchcase(name, branches):
                yield name


def find_branches(tree, branches_names):
    branches = None
    if isinstance(branches_names, str):
        branches = list(find_branches_by_string(tree, str.encode(branches_names)))
    if isinstance(branches_names, list):
        branches = []
        for b in branches_names:
            branches.extend(find_branches(tree, b))
    elif isinstance(branches_names, dict):
        branches = []
        for k, v in branches_names.items():
            sub = find_branches(tree[k], v)
            branches = [str.encode(k) + b'/' + b for b in sub]
    return branches


def get_dataframe(filepath, columns, batch_size, tree):
    file = uproot.open(filepath)
    tree_obj = file[tree]
    branches = []

    for b in find_branches(tree_obj, columns):
        if b'/' in b:
            steps = b.split(b'/')
            leaf = reduce(lambda branch, x: branch.get(x), steps, tree_obj)
            branches.append(leaf)
        else:
            branches.append(tree_obj.get(b))

    for df in tree_obj.pandas.iterate(lambda x: x in branches, entrysteps=batch_size):
        yield df
