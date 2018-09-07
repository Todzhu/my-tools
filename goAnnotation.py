#!/usr/bin/env python
#-*-coding:utf8-*-
#Function: Parsing gene ontology obo file then then get the input go's all parents(Version 1.0)
#Todzhu 2018.1.1

import re
class oboParse():
    def __init__(self,obofile):
        self.obofile = obofile
        self.go2name = {}
        self.go2namespace = {}
        self.go2parents = {}
        self.ancestors = []
        self.goparents = {}

    def parseObo(self):
        with open(self.obofile, 'r') as obo:
            obo = obo.read()
            Terms = obo.split('[Term]')
            for term in Terms:
                if re.search(r'id: GO:\d+', term):
                    go = re.search(r'id: (GO:\d+)', term).groups()[0]
                    name = re.search(r'name: (.*?)\n', term).groups()[0]
                    namespace = re.search(r'namespace: (.*?)\n', term).groups()[0]
                    self.go2name[go] = name
                    self.go2namespace[go] = namespace
                if re.search(r'is_a: GO:\d+', term):
                    go_parents = re.findall(r'is_a: (GO:\d+)', term)
                    self.go2parents[go] = go_parents
                if re.search(r'relationship: part_of GO:\d+', term):
                    go_part_of = re.findall(r'relationship: part_of (GO:\d+)', term)
                    if len(go_part_of) > 0 :
                        for part_of in go_part_of:
                            self.go2parents.setdefault(go, []).append(part_of)

    def parseAncestors(self):
        for go in self.ancestors:
            if go in self.go2parents:
                self.goparents[go] = self.go2parents[go]
            else:
                self.goparents[go] = 'root'
        return self.goparents

    def getAncestors(self,goid):
        self.ancestors.append(goid)
        if goid in self.go2parents:
            parents = self.go2parents[goid]
            if len(parents) > 0:
                for parent in parents:
                    self.ancestors.extend(self.getAncestors(parent))
        return self.parseAncestors()

if __name__ == '__main__':
    obo = oboParse('go-basic.obo')
    obo.parseObo()
    print(obo.getAncestors('GO:0000001'))



# 对于有向无环图的拓扑结构树，找出从起点到终点的所有路径
# def find_all_paths(graph, start, end, path=[]):
#     path = path + [start]
#     if start == end:
#         return [path]
#     if start not in graph:
#         return []
#     paths = []
#     for node in graph[start]:
#         if node not in path:
#             newpaths = find_all_paths(graph, node, end, path)
#             for newpath in newpaths:
#                 paths.append(newpath)
#     return paths
#
# def goTermLeve(graph, start, end, path=[]):
#     path = path + [start]
#     if start == end:
#         return path
#     if start not in graph:
#         return None
#     longest = None
#     for node in graph[start]:
#         if node not in path:
#             newpath = goTermLeve(graph, node, end, path)
#             if newpath:
#                 if not longest or len(newpath) > len(longest):
#                     longest = newpath
#     return longest
#