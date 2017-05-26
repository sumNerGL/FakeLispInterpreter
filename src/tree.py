def string_element(s):
    r = '"'
    ec = False
    for i, e in enumerate(s[1:]):
        r += e
        if ec:
            ec = False
            continue
        elif e == '\\':
            ec = True
        elif e == '"':
            break
    return r


def common_element(s):
    r = ''
    if s[0] == '"':
        r = string_element(s)
        return r
    for i, e in enumerate(s):
        if e in ') ':
            r = s[:i]
            break
    return r

# st1 = 'foo 2.34 (- 3 bar))'
# st2 = 'bar))'
# print(common_element(st1))
# print(common_element(st2))


def fomatted_element(s):
    num = '0123456789'
    if s[0] in num:
        if '.' in s:
            return float(s)
        else:
            return int(s)
    else:
        return s

# e1 = 'foo'
# e2 = '3.14'
# e3 = '3'
#
# print(type_element(e1))
# print(type_element(e2))
# print(type_element(e3))


def list2(s):
    l = []
    count = 0
    for i, e in enumerate(s):
        if count > 0:
            count -= 1
            continue
        elif e in '()':
            l.append(e)
        elif e == ' ':
            pass
        else:
            token = common_element(s[i:])
            count = len(token) - 1
            token = fomatted_element(token)
            l.append(token)
    return l

# s1 = '(+ 1 2 (- 3 4))'
# s2 = '(+ 12 2.34 (- 345 45))'
# s3 = '(+ foo 2.34 (- 3 bar))'
# s4 = '(+ foo 2.34 (- 3 "hi(\\" )"))'
#
# print(list2(s1))
# print(list2(s2))
# print(list2(s3))
# print(list2(s4))


def list_element(l):
    r = []
    count = 0
    self_count = 0
    for i, e in enumerate(l):
        if count > 0:
            count -= 1
            continue
        self_count += 1
        if e == ')':
            break
        elif e == '(':
            le, child_count = list_element(l[i+1:])
            count = child_count
            self_count += child_count
            r.append(le)
        else:
            r.append(e)
    return r, self_count


def tree(s):
    l = list2(s)
    r, c = list_element(l)
    return r[0]

# s1 = '(+ 1 2 (- 3 4))'
# s2 = '(+ 12 2.34 (- 345 45))'
# s3 = '(+ foo 2.34 (- 3 bar))'
# s4 = '(+ foo 2.34 (- 3 "hi(\\" )"))'
# s5 = '(+ foo 2.34 (- 3 bar) (- 3 bar))'
#
# print(s1, '>>>', tree(s1))
# print(s2, '>>>', tree(s2))
# print(s3, '>>>', tree(s3))
# print(s4, '>>>', tree(s4))
# print(s5, '>>>', tree(s5))
