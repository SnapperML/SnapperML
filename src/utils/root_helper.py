# Add support to load/save from/to S3
# Add connection to models part
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
    if b"*" in branches or b"?" in branches or b"[" in branches:
        for name, branch in tree.iteritems(recursive=True):
            if name == branches or glob.fnmatch.fnmatchcase(name, branches):
                yield branch.name


def find_branches(tree, branches_names):
    branches = None
    if isinstance(branches_names, str):
        branches = list(find_branches_by_string(tree, str.encode(branches_names)))
    if isinstance(branches_names, list):
        branches = []
        for b in branches_names:
            branches.extend(tree.matches(b))
    elif isinstance(branches_names, dict):
        branches = []
        for k, v in branches_names.items():
            sub = find_branches(tree[k], v)
            branches = [str.encode(k) + b'/' + b for b in sub]
    return branches


def get_dataframe(filepath, columns, batch_size, tree_path):
    file = uproot.open(filepath)
    tree = file[tree_path]

    branches = []
    for b in find_branches(tree, columns):
        if b'/' in b:
            steps = b.split(b'/')
            leaf = reduce(lambda branch, x: branch.get(x), steps, tree)
            branches.append(leaf)
        else:
            branches.append(tree.get(b))

    for df in tree.pandas.iterate(filepath, tree_path, lambda x: x in branches, entrysteps=batch_size):
        yield df
