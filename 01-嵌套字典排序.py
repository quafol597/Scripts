import json
import time

body = {
    'a': 1,
    'c': {
        'd': 4,
        'f': 6,
        'g': {
            'z': 6,
            'y': {
                'c': 4,
                'a': 5
            }
        },
        'e': 5,
    },
    'b': 2,
}


print(body)



def iterative_sort_test(v):
    """三重嵌套字典排序: 为了找规律"""
    for k0, v0 in v.items():
        if isinstance(v0, dict):
            v0 = dict(sorted(v0.items(), key=lambda item:item[0]))

            for k1, v1 in v0.items():
                if isinstance(v1, dict):
                    v1 = dict(sorted(v1.items(), key=lambda item:item[0]))

                    for k2, v2 in v1.items():
                        if isinstance(v2, dict):
                            v2 = dict(sorted(v2.items(), key=lambda item:item[0]))
                            v1[k2] = v2

                    v0[k1] = v1

            v[k0] = v0
    return v


# def iterative_sort(v0):
#     """多重嵌套字典排序: Finished"""
#     for k, v in v0.items():
#         if isinstance(v, dict):
#             v = dict(sorted(v.items(), key=lambda item:item[0]))
#             iterative_sort(v)
#             v0[k] = v
#     return v0


def iterative_sort(value):
    v0 = {'value': value}
    def inner(v0):
        """多重嵌套字典排序: Finished"""
        for k, v in v0.items():
            if isinstance(v, dict):
                v = dict(sorted(v.items(), key=lambda item:item[0]))
                inner(v)
                v0[k] = v
        return v0
    ret = inner(v0)
    return ret['value']


# body2 = iterative_sort_test({'body': body})
body2 = iterative_sort(body)

print(body2)
