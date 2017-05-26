from tree import tree

def ensure(condition, message):
    if not condition:
        print('*** 测试失败:', message)
    else:
        print('*** 测试成功:', message)


class Apply:
    def __init__(self, var=None, func=None):
        if var is None:
            var = {}
        if func is None:
            func = {}

        self.var = var
        self.func = func

    def plus(self, l):
        r = self.apply(l[1])
        for i, e in enumerate(l):
            if i < 2:
                continue
            r += self.apply(e)
        return r

    def minus(self, l):
        r = self.apply(l[1])
        for i, e in enumerate(l):
            if i < 2:
                continue
            r -= self.apply(e)
        return r

    def times(self, l):
        r = self.apply(l[1])
        for i, e in enumerate(l):
            if i < 2:
                continue
            r *= self.apply(e)
        return r

    def divide(self, l):
        r = self.apply(l[1])
        for i, e in enumerate(l):
            if i < 2:
                continue
            r /= self.apply(e)
        return r

    def calc_common(self, l, t):
        for i, e in enumerate(l):
            # print('i, e', i, e)
            if e in t:
                # print('if in')
                token = self.apply([e, l[i-1], l[i+1]])
                r = l[:i-1] + [token] + l[i+2:]
                # print('r', r)
                return r

    def calc_list(self, l):
        for i, e in enumerate(l):
            # print('i, e', i, e)
            if type(e) == list:
                t = self.calc(['calc', e])
                r = l[:i] + [t] + l[i+1:]
                return r

    def calc_apply(self, l):
        for i, e in enumerate(l):
            if type(e) == list:
                r = self.calc_list(l)
                return r
        if ('*' in l) or ('/' in l):
            r = self.calc_common(l, ['*', '/'])
            return r
        elif ('+' in l) or ('-' in l):
            r = self.calc_common(l, ['+', '-'])
            return r

    def calc(self, l):
        f = l[1]
        if len(f) > 1:
            t = self.calc_apply(f)
            r = self.calc(['calc', t])
        else:
            r = f[0]
        return r


    def judge(self, l):
        # l 的格式是 ['if', 条件表达式, 条件为 True 时, 条件为 False 时]
        if self.apply(l[1]) is True:
            return self.apply(l[2])
        else:
            return self.apply(l[3])

    def greater_than(self, l):
        r = self.apply(l[1]) > self.apply(l[2])
        return r

    def less_than(self, l):
        r = self.apply(l[1]) < self.apply(l[2])
        return r

    def equal(self, l):
        r = self.apply(l[1]) == self.apply(l[2])
        return r

    def define_variable(self, l):
        v = self.apply(l[2])
        k = l[1]
        r = {
            k: v,
        }
        self.var.update(r)
        # print(self.var)
        return 'N/A'

    def call_variable(self, name):
        return self.var[name]

    def define_function(self, l):
        k = l[1]
        v = [l[2], l[3]]
        r = {
            k: v,
        }
        self.func.update(r)
        return 'N/A'

    def func_var_dict(self, k, v):
        r = {}
        for i, e in enumerate(k):
            r[e] = self.apply(v[i])
        return r

    def call_function(self, l):
        name = l[1]
        var_value = l[2]

        func = self.func[name]
        func_var = func[0]
        func_tree = func[1]

        func_var_dict = self.func_var_dict(func_var, var_value)
        temp_var_dict = self.var.copy()
        temp_var_dict.update(func_var_dict)

        r = Apply(temp_var_dict, self.func).apply_trees(func_tree)
        return r

    def apply(self, l):
        ops = {
            '+': self.plus,
            '-': self.minus,
            '*': self.times,
            '/': self.divide,
            'calc': self.calc,
            'if': self.judge,
            '>': self.greater_than,
            '<': self.less_than,
            '=': self.equal,
            'var': self.define_variable,
            'def': self.define_function,
            'call': self.call_function,
        }

        if type(l) == list:
            op = l[0]
            r = ops[op](l)
        elif type(l) == str:
            r = self.call_variable(l)
        else:
            r = l
        return r

    def apply_trees(self, l):
        r = []
        for i, e in enumerate(l):
            # if e[0] == 'var':
            #     self.var.update(self.define_variable(e))
            #     r.append('N/A')
            # if e[0] == 'def':
            #     self.func.update(self.define_function(e))
            #     r.append('N/A')
            # if e[0] == 'call':
            #     t = self.call_function(e)
            #     r.append(t)
            # else:
            token = self.apply(e)
            r.append(token)
        return r[-1]


def test_plus():
    l1 = ['+', 1, 2]
    l2 = ['+', 1, 2, ['+', 1, 2]]

    ensure(Apply().plus(l1) == 3, 'plus 测试1')
    ensure(Apply().plus(l2) == 6, 'plus 测试2')


def test_minus():
    l1 = ['-', 2, 1]
    l2 = ['-', 5, 2, ['+', 1, 2]]

    ensure(Apply().minus(l1) == 1, 'decrease 测试1')
    ensure(Apply().minus(l2) == 0, 'decrease 测试2')


def test_times():
    l1 = ['*', 2, 1]
    l2 = ['*', 5, 2, ['+', 1, 2]]

    ensure(Apply().times(l1) == 2, 'times 测试1')
    ensure(Apply().times(l2) == 30, 'times 测试2')


def test_divide():
    l1 = ['/', 2, 2]
    l2 = ['/', 30, 2, ['+', 1, 2]]

    ensure(Apply().divide(l1) == 1, 'divide 测试1')
    ensure(Apply().divide(l2) == 5, 'divide 测试2')


def test_calc():
    l1 = ['calc', [1, '+', 2, '-', 3]]
    l2 = ['calc', [1, '+', 2, '*', 3, '/', 2]]
    l3 = ['calc', [1, '+', 2, '*', [1, '+', [1, '+', 1]], '/', 2]]

    ensure(Apply().calc(l1) == 0, 'calc 测试1')
    ensure(Apply().calc(l2) == 4, 'calc 测试2')
    ensure(Apply().calc(l3) == 4, 'calc 测试3')


def test_judge():
    l1 = ['if', True, 1, 2]
    l2 = ['if', False, 2, ['+', 1, 2]]
    l3 = ['if', False, 2, ['if', True, 1, 2]]

    ensure(Apply().judge(l1) == 1, 'judge 测试1')
    ensure(Apply().judge(l2) == 3, 'judge 测试2')
    ensure(Apply().judge(l3) == 1, 'judge 测试3')


def test_greater_than():
    l1 = ['>', 2, 1]
    l2 = ['>', 1, 2]
    l3 = ['>', 1, ['+', 1, 1]]

    ensure(Apply().greater_than(l1), 'more 测试1')
    ensure(not Apply().greater_than(l2), 'more 测试2')
    ensure(not Apply().greater_than(l3), 'more 测试3')


def test_less_than():
    l1 = ['<', 2, 1]
    l2 = ['<', 1, 2]
    l3 = ['<', 1, ['+', 1, 1]]

    ensure(not Apply().less_than(l1), 'less 测试1')
    ensure(Apply().less_than(l2), 'less 测试2')
    ensure(Apply().less_than(l3), 'less 测试3')


def test_equal():
    l1 = ['=', 2, 1]
    l2 = ['=', 2, 2]
    l3 = ['=', 2, ['+', 1, 1]]

    ensure(not Apply().equal(l1), 'equal 测试1')
    ensure(Apply().equal(l2), 'equal 测试2')
    ensure(Apply().equal(l3), 'equal 测试3')


def test_define_variable():
    l1 = ['var', 'a', 2]
    l2 = ['var', 'a', ['-', 2, 1]]

    ensure(Apply().define_variable(l1) == 'N/A', 'define_variable 测试1')
    ensure(Apply().define_variable(l2) == 'N/A', 'define_variable 测试2')


def test_define_function():
    l1 = ['def', 'f1', ['a', 'b'], ['if', ['<', 'a', 0], 3, 'b']]
    l2 = ['def', 'f2', [], [['-', 2, 2], ['-', 2, 1]]]

    ensure(Apply().define_function(l1) == 'N/A', 'define_function 测试1')
    ensure(Apply().define_function(l2) == 'N/A', 'define_function 测试2')


def test_call_function():
    d1 = [['def', 'f1', ['a', 'b'], [['if', ['<', 'a', 0], 3, 'b']]]]
    apply = Apply()
    apply.apply_trees(d1)
    # print('func', self.func)
    l1 = ['call', 'f1', [1, 2]]
    ensure(apply.call_function(l1) == 2, 'call_function 测试1')


def test_apply():
    l1 = ['+', 1, 2, ['-', 2, 1]]
    l2 = ['if', ['>', 1, 2], 1, 2]
    l3 = ['if', ['<', 1, 2], 1, 2]
    l4 = ['if', ['=', 1, 2], 1, 2]

    # print(apply(l1))
    # print(apply(l2))
    # print(apply(l3))
    # print(apply(l4))

    ensure(Apply().apply(l1) == 4, 'apply 测试1')
    ensure(Apply().apply(l2) == 2, 'apply 测试2')
    ensure(Apply().apply(l3) == 1, 'apply 测试3')
    ensure(Apply().apply(l4) == 2, 'apply 测试4')


def test_apply_trees():
    l1 = [['+', 1, 2, ['-', 2, 1]]]
    l2 = [['-', 2, 2], ['-', 2, 1]]
    l3 = [['var', 'a', ['-', 2, 1]]]
    l4 = [['var', 'a', 1], ['var', 'b', ['+', 1, 1]], ['if', ['<', 'a', 0], 3, 'b']]
    l5 = [
        ['var', 'a', 3],
        ['var', 'b', 2],
        ['def', 'f1', ['a', 'b'], [['-', ['+', 'a', 2], 3, 'b']]],
        ['call', 'f1', ['a', 'b']]
    ]

    ensure(Apply().apply_trees(l1) == 4, 'apply_trees 测试1')
    ensure(Apply().apply_trees(l2) == 1, 'apply_trees 测试2')
    ensure(Apply().apply_trees(l3) == 'N/A', 'apply_trees 测试3')
    ensure(Apply().apply_trees(l4) == 2, 'apply_trees 测试4')
    ensure(Apply().apply_trees(l5) == 0, 'apply_trees 测试5')


def test():
    test_plus()
    test_minus()
    test_times()
    test_divide()
    test_calc()
    test_judge()
    test_greater_than()
    test_less_than()
    test_equal()
    test_define_variable()
    test_define_function()
    test_call_function()

    test_apply()

    test_apply_trees()

# test()


def preview():
    test_list = []

    # test_list1 = [['+', 1, 2, ['-', 2, 1]]]
    test_list1 = '((+ 1 2 (- 2 1)))'
    # test_list2 = [['var', 'a', 1], ['var', 'b', ['+', 1, 1]], ['if', ['<', 'a', 0], 3, 'b']]
    test_list2 = '((var a 1) (var b (+ 1 1)) (if (< a 0) 3 b))'
    # test_list3 = [
    #     ['var', 'a', 3],
    #     ['var', 'b', 2],
    #     ['def', 'f1', ['a', 'b'], [['-', ['+', 'a', 2], 3, 'b']]],
    #     ['call', 'f1', ['a', 'b']]
    # ]
    test_list3 = '((var a 3) (var b 2) (def f1 (a b) ((- (+ a 2) 3 b))) (call f1 (a b)))'
    # test_list4 = [
    #     ['var', 'a', 4],
    #     ['def', 'f1', ['n'],
    #      [
    #         ['if', ['<', 'n', 2], 1,
    #          ['*', 'n', ['call', 'f1', [['-', 'n', 1]]]]
    #          ]
    #      ]
    #      ],
    #     ['call', 'f1', ['a']]
    # ]
    test_list4 = '((var a 4) (def f1 (n) ((if (< n 2) 1 (* n (call f1 ((- n 1))))))) (call f1 (a)))'
    # test_list5 = [['calc', [1, '+', 2, '*', [1, '+', [1, '+', 1]], '/', 2]]]
    test_list5 = '((calc (1 + 2 * (1 + (1 + 1)) / 2)))'

    test_list.append(test_list1)
    test_list.append(test_list2)
    test_list.append(test_list3)
    test_list.append(test_list4)
    test_list.append(test_list5)

    for i, e in enumerate(test_list):
        print(e)
        l = tree(e)
        print('>>>', l)
        r = Apply().apply_trees(l)
        print('>>>', r)
        print()

# preview()

if __name__ == '__main__':
    # test()
    preview()

