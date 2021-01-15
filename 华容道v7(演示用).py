#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time  : 2020/12/22 1:27
# @Author: Vince Wu
# @File  : 华容道.py

import sys
import time
import math
from collections import deque
import random as rd

man_size = {0: 9, 1: 4, 3: 2, 5: 2, 4: 2, 6: 2, 2: 3, 7: 1, 8: 1, 9: 1, 10: 1}
is_searched = {0: 1}
init_matrix = [3, 1, 1, 5, 3, 1, 1, 5, 4, 2, 2, 6, 4, 8, 9, 6, 7, 0, 0, 10]
# init_matrix = [3,2,2,7,3,1,1,5,4,1,1,5,4,8,6,9,0,10,6,0]
search_deque = deque()
total_search = 0


class Step(object):  #棋盘类

    is_searched = {0: 1}  # 已搜索过的棋盘，字典
    total_search = 0  # 步数

    def __init__(self, matrix, father=None):
        self.matrix = matrix  #棋盘状态
        self.father = father  # 父棋盘，用于回溯生成解的每一步

    def hash(self):  # 剪枝
        hash_mod = []
        for i in self.matrix:  # 等价节点剪枝
            # 复制一个棋盘，其中相同类型的棋子有相同的值，如竖将都为2
            if 7 <= i <= 10:
                hash_mod.append(4)
            elif 3 <= i <= 6:
                hash_mod.append(2)
            elif i == 0:
                hash_mod.append(0)
            elif i == 2:
                hash_mod.append(3)
            else:
                hash_mod.append(1)

        try:  # 已搜索过
            is_searched[tuple(hash_mod)] += 1
            return 1
        except KeyError:  # 未搜索过
            is_searched[tuple(hash_mod)] = 1
            for i in range(0, 20, 4):  # 镜像节点剪枝，将对称的棋盘加入已搜索
                hash_mod[i], hash_mod[i + 1], hash_mod[i + 2], hash_mod[i + 3] =\
                 hash_mod[i + 3], hash_mod[i + 2], hash_mod[i + 1], hash_mod[i]
            is_searched[tuple(hash_mod)] = 1
            return 0

    # A1 判断
    def find_way(self):
        for man_num in range(0, 20):
            if self.matrix[man_num] == 0:
                if man_num - 4 >= 0 and self.matrix[man_num - 4] != 0:
                    self.move(man_num, 'up')
                if man_num <= 15 and self.matrix[man_num + 4] != 0:
                    self.move(man_num, 'down')
                if man_num % 4 != 0 and self.matrix[man_num - 1] != 0:
                    self.move(man_num, 'left')
                if man_num % 4 != 3 and man_num <= 18 and self.matrix[man_num + 1] != 0:
                    self.move(man_num, 'right')

    # A2 判断
    def move(self, man_num, direction):
        global search_deque
        flag = self.matrix.copy()
        if direction == 'up':
            if self.matrix[man_num - 4] == 1:  # 上方是曹操
                try:
                    if self.matrix[man_num - 4 + 1] == 1 and self.matrix[man_num + 1] == 0 and man_num - 4 + 1 >= 0:  # 曹操位置
                        flag[man_num], flag[man_num + 1] = 1, 1
                        flag[man_num - 8], flag[man_num - 7] = 0, 0
                except IndexError:
                    1
                finally:
                    try:
                        if self.matrix[man_num - 5] == 1 and self.matrix[man_num - 1] == 0 and man_num - 4 - 1 >= 0:
                            flag[man_num], flag[man_num - 1] = 1, 1
                            flag[man_num - 8], flag[man_num - 9] = 0, 0
                    except IndexError:
                        1
                    finally:
                        0
            elif man_size[self.matrix[man_num - 4]] == 2 and man_num - 8 >= 0:  # 上方是竖将
                flag[man_num] = self.matrix[man_num - 4]
                flag[man_num - 4] = self.matrix[man_num - 8]
                flag[man_num - 8] = 0
            elif man_size[self.matrix[man_num - 4]] == 3 and man_num - 4 >= 0:  # 上方是横将
                try:
                    if man_size[self.matrix[man_num - 4 + 1]] == 3 and self.matrix[man_num + 1] == 0:  # 曹操位置
                        flag[man_num], flag[man_num + 1] = self.matrix[man_num - 4], self.matrix[man_num - 4]
                        flag[man_num - 4], flag[man_num - 3] = 0, 0
                finally:
                    try:
                        if man_size[self.matrix[man_num - 5]] == 3 and self.matrix[man_num - 1] == 0:
                            flag[man_num], flag[man_num - 1] = self.matrix[man_num - 4], self.matrix[man_num - 4]
                            flag[man_num - 4], flag[man_num - 5] = 0, 0
                    finally:
                        0
            else:  # 上方是小兵
                flag[man_num] = self.matrix[man_num - 4]
                flag[man_num - 4] = 0

            # try:
            #     if self.matrix[man_num + 4] == 1:  # 下方是曹操
            #         try:
            #             if self.matrix[man_num + 4 + 1] == 1 and self.matrix[man_num + 1] == 0:  # 曹操位置
            #                 self.matrix[man_num], self.matrix[man_num + 1] = 1, 1
            #                 self.matrix[man_num + 4], self.matrix[man_num + 5] = 0, 0
            #         finally:
            #             try:
            #                 if self.matrix[man_num + 3] == 1 and self.matrix[man_num - 1] == 0:
            #                     self.matrix[man_num], self.matrix[man_num - 1] = 1, 1
            #                     self.matrix[man_num + 4], self.matrix[man_num + 3] = 0, 0
            #             finally:
            #                 nothing = 0
            # finally:
            #     try:
            #         if self.matrix[man_num + 1]

        elif direction == 'down':  # 下方
            if self.matrix[man_num + 4] == 1:  # 是曹操
                try:
                    if self.matrix[man_num + 4 + 1] == 1 and self.matrix[man_num + 1] == 0:  # 曹操位置
                        flag[man_num], flag[man_num + 1] = 1, 1
                        flag[man_num + 8], flag[man_num + 9] = 0, 0
                finally:
                    try:
                        if self.matrix[man_num + 4 - 1] == 1 and self.matrix[man_num - 1] == 0 and man_num % 4 != 0:
                            flag[man_num], flag[man_num - 1] = 1, 1
                            flag[man_num + 8], flag[man_num + 7] = 0, 0
                    finally:
                        0
            elif man_size[self.matrix[man_num + 4]] == 2:  # 是竖将
                # a = self
                # while a.father is not None:
                #     print(a.matrix)
                #     a = a.father
                flag[man_num] = self.matrix[man_num + 4]
                flag[man_num + 4] = self.matrix[man_num + 8]
                flag[man_num + 8] = 0

            elif man_size[self.matrix[man_num + 4]] == 3:  # 是横将
                try:
                    if man_size[self.matrix[man_num + 4 + 1]] == 3 and self.matrix[man_num + 1] == 0:  # 位置
                        flag[man_num], flag[man_num + 1] = self.matrix[man_num + 4], self.matrix[man_num + 4]
                        flag[man_num + 4], flag[man_num + 5] = 0, 0
                except IndexError:
                    0
                finally:
                    try:
                        if man_size[self.matrix[man_num + 3]] == 3 and self.matrix[man_num - 1] == 0 and man_num % 4 != 0:
                            flag[man_num], flag[man_num - 1] = self.matrix[man_num + 4], self.matrix[man_num + 4]
                            flag[man_num + 4], flag[man_num + 3] = 0, 0
                    finally:
                        0
            else:  # 是小兵
                flag[man_num] = self.matrix[man_num + 4]
                flag[man_num + 4] = 0

        elif direction == 'left':  # left
            if self.matrix[man_num - 1] == 1:  # 是曹操
                try:
                    if self.matrix[man_num - 1 + 4] == 1 and self.matrix[man_num + 4] == 0:  # 曹操位置 down
                        flag[man_num], flag[man_num + 4] = 1, 1
                        flag[man_num - 2], flag[man_num - 2 + 4] = 0, 0
                except IndexError:
                    0
                finally:
                    try:
                        if self.matrix[man_num - 4 - 1] == 1 and self.matrix[man_num - 4] == 0 and man_num - 4 - 1 >= 0:
                            flag[man_num], flag[man_num - 4] = 1, 1
                            flag[man_num - 2], flag[man_num - 6] = 0, 0
                    finally:
                        0

            elif man_size[self.matrix[man_num - 1]] == 3 and man_num - 1 >= 0:  # 是横将
                flag[man_num] = self.matrix[man_num - 1]
                flag[man_num - 1] = self.matrix[man_num - 2]
                flag[man_num - 2] = 0

            elif man_size[self.matrix[man_num - 1]] == 2 and man_num - 1 >= 0:  # 是竖将
                try:
                    if self.matrix[man_num - 1 + 4] == self.matrix[man_num - 1] and \
                            self.matrix[man_num + 4] == 0:  # 位置down
                        flag[man_num], flag[man_num + 4] = self.matrix[man_num - 1], self.matrix[man_num - 1]
                        flag[man_num - 1], flag[man_num + 3] = 0, 0
                except IndexError:
                    0
                finally:
                    try:
                        if self.matrix[man_num - 5] == self.matrix[man_num - 1] and \
                                self.matrix[man_num - 4] == 0 and man_num - 5 >= 0:
                            flag[man_num], flag[man_num - 4] = self.matrix[man_num - 1], self.matrix[man_num - 1]
                            flag[man_num - 1], flag[man_num - 5] = 0, 0
                    except IndexError:
                        0
                    finally:
                        0
            elif man_num - 1 >= 0 and man_size[self.matrix[man_num - 1]] == 1:  # 是小兵
                flag[man_num] = self.matrix[man_num - 1]
                flag[man_num - 1] = 0

        else:  # right
            if self.matrix[man_num + 1] == 1:  # 是曹操
                try:
                    if self.matrix[man_num + 1 + 4] == 1 and \
                            self.matrix[man_num + 4] == 0:  # 曹操位置 down
                        flag[man_num], flag[man_num + 4] = 1, 1
                        flag[man_num + 2], flag[man_num + 2 + 4] = 0, 0
                except IndexError:
                    0
                finally:
                    try:
                        if self.matrix[man_num - 4 + 1] == 1 and self.matrix[man_num - 4] == 0:
                            flag[man_num], flag[man_num - 4] = 1, 1
                            flag[man_num + 2], flag[man_num + 2 - 4] = 0, 0
                    finally:
                        0

            elif man_size[self.matrix[man_num + 1]] == 3:  # 是横将
                flag[man_num] = self.matrix[man_num + 1]
                flag[man_num + 1] = self.matrix[man_num + 2]
                flag[man_num + 2] = 0

            elif man_size[self.matrix[man_num + 1]] == 2:  # 是竖将
                try:
                    if self.matrix[man_num + 1 + 4] == self.matrix[man_num + 1] and self.matrix[man_num + 4] == 0:  # 位置down
                        flag[man_num], flag[man_num + 4] = self.matrix[man_num + 1], self.matrix[man_num + 1]
                        flag[man_num + 1], flag[man_num + 5] = 0, 0
                except IndexError:
                    0
                finally:
                    try:
                        if self.matrix[man_num + 1 - 4] == self.matrix[man_num + 1] and self.matrix[man_num - 4] == 0:
                            flag[man_num], flag[man_num - 4] = self.matrix[man_num + 1], self.matrix[man_num + 1]
                            flag[man_num + 1], flag[man_num - 3] = 0, 0
                    finally:
                        0
            else:  # 是小兵
                flag[man_num] = self.matrix[man_num + 1]
                flag[man_num + 1] = 0

        son = Step(flag, self)
        # print(flag)
        if flag[17] == 1 and flag[18] == 1:
            total_step = 1
            while son.father is not None:
                print('father', total_step, son.matrix)
                son = son.father
                total_step += 1
            print('总步数: ', total_step)
            time_end = time.time()
            print('total time:', time_end - time_start)
            sys.exit(0)
        search_deque += [son]

# 开始搜索
def search(init_matrix):
    global search_deque
    init_step = Step(init_matrix, None)
    search_deque += [init_step]
    while search_deque:
        searching = search_deque.popleft()
        if searching.hash():
            continue
        searching.find_way()

    # print("No Solution", )
    # time_end = time.time()
    # print('total time:', time_end - time_start)
    return 1  # unsuccessful

# 随机生成一个棋盘
def generate(always_feasible = False):
    empty_cb = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    for i in range(1, 11):
        while True:
            num = math.floor(rd.random() * 19.999)
            if i == 1 and num % 4 != 3 and num <= 10 and max(empty_cb[num], empty_cb[num + 1], empty_cb[num + 4], empty_cb[num + 5]) == 0:
                empty_cb[num], empty_cb[num + 1], empty_cb[num + 4], empty_cb[num + 5] = 1, 1, 1, 1
                # print(empty_cb)
                break
            elif i == 2 and num % 4 != 3 and max(empty_cb[num], empty_cb[num + 1]) == 0:
                empty_cb[num], empty_cb[num + 1] = 2, 2
                # print(empty_cb)
                break
            elif 3 <= i <= 6 and num <= 15 and max(empty_cb[num], empty_cb[num + 4]) == 0:
                empty_cb[num], empty_cb[num + 4] = i, i
                # print(empty_cb)
                break
            elif 7 <= i <= 10 and empty_cb[num] == 0:
                empty_cb[num] = i
                # print(empty_cb)
                break
    print(empty_cb)
    return empty_cb


#随机生成一个有解的棋盘
def generate_always_feasible():
    while search(generate()):
        1

# 主函数
if __name__ == '__main__':
    time_start = time.time()
    # generate_always_feasible()
    print("无解!" if search(generate()) else "")
    # print(init_matrix)
    # search([6, 1, 1, 5, 6, 1, 1, 5, 4, 2, 2, 3, 4, 7, 8, 3, 0, 9, 0, 10])
    print(time.time() - time_start)