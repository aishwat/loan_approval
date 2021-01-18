# https://github.com/openvenues/libpostal
# https://github.com/openvenues/pypostal
# https://towardsdatascience.com/natural-language-processing-for-fuzzy-string-matching-with-python-6632b7824c49
from postal.parser import parse_address
from fuzzywuzzy import fuzz
from datetime import date

# from postal.expand import expand_address

def get_dict(add):
    d = dict()
    for k, v in add:
        # address format => https: // github.com / OpenCageData / address - formatting
        # house number issue => https://github.com/openvenues/libpostal/issues/304
        if v == "house_number" or v == "house":
            d["house"] = k
        else:
            d[v] = k
    return d


def matchAddress(a1, a2):
    # return fuzz.ratio(a1.lower(), a2.lower())
    add1 = parse_address(a1.lower())  # returns tuples in v:k format
    add2 = parse_address(a2.lower())
    d1 = get_dict(add1)
    d2 = get_dict(add2)
    # pp.pprint(expand_address(a1.lower()))
    # print(d1)
    # print(d2)
    all_keys = list(set().union(list(d1.keys()), list(d2.keys())))
    count = 0
    s = 0
    for k in all_keys:
        r = fuzz.ratio(d1.get(k, ''), d2.get(k, ''))
        print("{} has {}% match => {} || {}".format(k, r, d1.get(k, ''), d2.get(k, '')))
        s += r
        count += 100
    return (s / count) * 100


def roundup(x):
    return x if x % 100 == 0 else x + (-x) % 100

def calculateAge(born):
    today = date.today()
    try:
        birthday = born.replace(year=today.year)
    # raised when birth date is February 29
    # and the current year is not a leap year
    except ValueError:
        birthday = born.replace(year=today.year,
                                month=born.month + 1, day=1)

    if birthday > today:
        return today.year - born.year - 1
    else:
        return today.year - born.year