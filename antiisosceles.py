# solving Riddler Classic @ https://fivethirtyeight.com/features/no-isosceles-triangles-for-you/

from itertools import combinations
import time


class Grid:
    def __init__(self, n):
        self.n = n
        self.points = sorted([(x, y) for x in range(n) for y in range(n)])
        self.point_indices = {p: i for i, p in enumerate(self.points)}
        self.distances = {}
        self.point_sets = {p: set() for p in self.points}
        for p0 in self.points:
            for p1 in self.points:
                if p0 < p1:
                    dist = self.calc_distance(p0, p1)
                    self.distances[(p0, p1)] = dist
                    self.point_sets[p0].add(dist)
                    self.point_sets[p1].add(dist)
        self.point_dicts = {p: {dist: set() for dist in self.point_sets[p]} for p in self.points}
        for ((p0, p1), dist) in self.distances.items():
            self.point_dicts[p0][dist].add(p1)
            self.point_dicts[p1][dist].add(p0)
        self.exclusions = {}
        for p0 in self.points:
            for p1 in self.points:
                if p0 < p1:
                    dist = self.distances[(p0, p1)]
                    excl = self.point_dicts[p0][dist].union(self.point_dicts[p1][dist])
                    excl.remove(p0)
                    excl.remove(p1)
                    for dist in self.point_sets[p0].intersection(self.point_sets[p1]):
                        new_excl = self.point_dicts[p0][dist].intersection(self.point_dicts[p1][dist])
                        excl = excl.union(new_excl)
                    self.exclusions[(p0, p1)] = excl

    @classmethod
    def calc_distance(cls, p0, p1):
        return (p0[0] - p1[0]) ** 2 + (p0[1] - p1[1]) ** 2

    def backtrack_antiisosceles_sets(
            self, curr_set=None, curr_best_score=0, curr_best_sets=None, start_index=0, show_partial=False
    ):
        if not curr_set:
            curr_set = set()
        if not curr_best_sets:
            curr_best_sets = set()
        score = len(curr_set)
        if score > curr_best_score:
            curr_best_score = score
            curr_best_sets = set([tuple(sorted(curr_set))])
            if show_partial:
                print((curr_best_score, curr_best_sets))
        elif score == curr_best_score:
            curr_best_sets.add(tuple(sorted(curr_set)))
        candidate_points = set(self.points[start_index:])
        for p0 in curr_set:
            for p1 in curr_set:
                if p0 < p1:
                    candidate_points = candidate_points.difference(self.exclusions[(p0, p1)])
        if candidate_points:
            for cp in candidate_points:
                curr_set.add(cp)
                start_index = self.point_indices[cp] + 1
                score, best_sets = self.backtrack_antiisosceles_sets(
                    curr_set, curr_best_score, curr_best_sets, start_index, show_partial
                )
                if score > curr_best_score:
                    curr_best_score = score
                    curr_best_sets = best_sets
                elif score == curr_best_score:
                    curr_best_sets = curr_best_sets.union(best_sets)
                curr_set.remove(cp)
        return curr_best_score, curr_best_sets

    @classmethod
    def set_is_antiisosceles(cls, test_set):
        for three_points in combinations(test_set, 3):
            if len(set([cls.calc_distance(p0, p1) for (p0, p1) in combinations(three_points, 2)])) < 3:
                print(f'The 3 points {three_points} are the vertices of an isosceles triangle.')
                return False
        return True

    @classmethod
    def set2str(cls, set2show, n):
        set2show = set(set2show)
        return '\n'.join([' '.join(['x' if (x, y) in set2show else '.' for x in range(n)]) for y in range(n)])


# print(Grid.set_is_antiisosceles(((0, 0), (0, 1), (1, 2), (2, 2))))  # True
# print(Grid.set_is_antiisosceles(((0, 0), (0, 1), (1, 2), (2, 1))))  # False


for n in range(2, 10):
    time0 = time.time()
    grid = Grid(n)
    best_score, best_sets = grid.backtrack_antiisosceles_sets()
    print(f'\nIn a grid {n} x {n}, the largest anti-isosceles sets are these {len(best_sets)} sets, '
          f'having size {best_score}:')
    for s in best_sets:
        print(s)
    sets_all_ok = True
    for test_set in best_sets:
        if not Grid.set_is_antiisosceles(test_set):
            sets_all_ok = False
            print(f'Wrong answer: The set {test_set} is not anti-isosceles.')
    if sets_all_ok:
        print('All sets have been validated.')
    time1 = time.time()
    print(f'Time needed for search: {(time1 - time0):.3f} seconds.')
    print('Showing the sets:')
    print('\n\n'.join([Grid.set2str(s, n) for s in best_sets]) +'\n')
