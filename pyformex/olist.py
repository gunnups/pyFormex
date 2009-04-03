# $Id$

"""Some convenient shortcuts for common list operations.

While most of these functions look (and work) like set operations, their
result differs from using Python builtin Sets in that they preserve the
order of the items in the lists.
"""


def union(a,b):
    """Return a list with all items in a or in b, in the order of a,b."""
    return a + [ i for i in b if i not in a ]


def difference(a,b):
    """Return a list with all items in a but not in b, in the order of a."""
    return [ i for i in a if i not in b ]


def symdifference(a,b):
    """Return a list with all items in a or b but not in both."""
    return difference(a,b) + difference(b,a)


def intersection (a,b):
    """Return a list with all items in a and  in b, in the order of a."""
    return [ i for i in a if i in b ]


def concatenate(a):
    """Concatenate a list of lists"""
    return reduce(list.__add__,a)


def flatten(a,recurse=False):
    """Flatten a nested list.

    By default, lists are flattened one level deep.
    If recurse=True, flattening recurses through all sublists.
    """
    r = []
    for i in a:
        if type(i) == list:
            if recurse:
                r.extend(flatten(i))
            else:
                r.extend(i)
        else:
            r.append(i)
    return r

    
def select(a,b):
    """Return a subset of items from a list.

    Returns a list with the items of a for which the index is in b.
    """
    return [ a[i] for i in b ]
        


def collectOnLength(items,return_indices=False):
    """Collect items of a list in separate bins according to the item length.

    items is a list of items of any type having the len() method.
    The items are put in separate lists according to their length.

    The return value is a dict where the keys are item lengths and
    the values are lists of items with this length.

    If return_indices is True, a second dict is returned, with the same
    keys, holding the original indices of the items in the lists.
    """
    if return_indices:
        res,ind = {},{}
        for i,item in enumerate(items):
            li = len(item)
            if li in res.keys():
                res[li].append(item)
                ind[li].append(i)
            else:
                res[li] = [ item ]
                ind[li] = [ i ]
        return res,ind
    else:
        res = {}
        for item in items:
            li = len(item)
            if li in res.keys():
                res[li].append(item)
            else:
                res[li] = [ item ]
        return res


if __name__ == "__main__":

    a = [1,2,3,5,6,7]
    b = [2,3,4,7,8,9]
    print a
    print b
    print union(a,b)
    print difference(a,b)
    print difference(b,a)
    print symdifference(a,b)
    print intersection(a,b)
    print select(a,[1,3])
    print concatenate([a,b,a])
    print flatten([1,2,a,[a]])
    print flatten([1,2,a,[a]],recurse=True)
      
    
# End