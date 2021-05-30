# antiisosceles
late solution to Riddler Classic @ https://fivethirtyeight.com/features/no-isosceles-triangles-for-you/

Contents:
- antiisosceles.py contains code finding all anti-isosceles sets of maximum size within a square grid by means of backtracking, considering all the points excluded by each partial set being considered
- output.txt contains the findings for all square grids from size 2 to 9, computed over about 4 hours on my MacBook Air, including Text Art-style visualizations of the maximum-size anti-isosceles sets

Maximum size of anti-isosceles sets by edge size of square grid:
2 -->  2
3 -->  4
4 -->  6
5 -->  7
6 -->  9
7 --> 10
8 --> 13
9 --> 16
