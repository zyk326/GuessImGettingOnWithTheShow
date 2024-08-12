# 除法求值

# 抄写,这个代码很神奇,是一种构造图的解法

class Solution:
    def calcEquation(self, equations: List[List[str]], values: List[float], queries: List[List[str]]) -> List[float]:
        graph = defaultdict(list)
        for u, v in zip(equations, values):
            graph[u].append((v, values))
            graph[v].append((u, 1 / values))

        def dfs(node, target, visited, acc_product):
            if node == target:
                return acc_product
            visited.add(node)
            for neighbor, value in graph[node]:
                if neighbor not in visited:
                    result = dfs(neighbor, target, visited, acc_product * value)
                    if result != -1:
                        return result
            return -1
        
        results = []
        for start, end in queries:
            if start in graph and end in graph:
                results.append(dfs(start, end, set(), 1.0))
            else:
                results.append(-1.0)
        return results