# 最终修正版main.py
from pathfinding.core.graph import Graph, GraphNode
from pathfinding.finder.a_star import AStarFinder
from itertools import permutations


class CityNode(GraphNode):
    """
    自定义城市节点类，添加坐标属性
    为兼容原路径规划库的启发式函数
    """

    def __init__(self, node_id, x=0, y=0):
        super().__init__(node_id)
        self.x = x  # 模拟坐标
        self.y = y  # 可根据实际需要设置真实坐标


def setup_graph():
    """创建带地理坐标的图结构"""
    # 定义节点坐标
    nodes = {
        'A': CityNode('A', x=0, y=0),
        'B': CityNode('B', x=1, y=0),
        'C': CityNode('C', x=2, y=1),
        'D': CityNode('D', x=1, y=2)
    }

    # 定义道路连接（使用实际节点对象）
    edges = [
        (nodes['A'], nodes['B'], 1), (nodes['B'], nodes['A'], 1),
        (nodes['B'], nodes['C'], 2),
        (nodes['C'], nodes['D'], 3),
        (nodes['D'], nodes['A'], 4), (nodes['A'], nodes['D'], 4),
        (nodes['B'], nodes['D'], 5), (nodes['D'], nodes['B'], 5)
    ]

    return Graph(edges=edges, nodes=nodes, bi_directional=False)


def calculate_paths(graph, locations):
    """增强型路径预计算"""
    path_cost = {}
    path_sequence = {}
    from pathfinding.core.diagonal_movement import DiagonalMovement
    finder = AStarFinder(diagonal_movement=DiagonalMovement.never)

    for start_id in locations:
        for end_id in locations:
            if start_id == end_id:
                path_cost[(start_id, end_id)] = 0
                path_sequence[(start_id, end_id)] = []
                continue

            start_node = graph.node(start_id)
            end_node = graph.node(end_id)
            path, _ = finder.find_path(start_node, end_node, graph)

            if path:
                path_cost[(start_id, end_id)] = path[-1].g
                path_sequence[(start_id, end_id)] = [n.node_id for n in path]
            else:
                print(f"路径不存在: {start_id} -> {end_id}")
                path_cost[(start_id, end_id)] = float('inf')
                path_sequence[(start_id, end_id)] = []

    return path_cost, path_sequence


def find_optimal_route(start, points, path_cost):
    """寻找最优访问顺序"""
    min_cost = float('inf')
    best_order = None

    for perm in permutations(points):
        # 计算路径成本: start -> p1 -> p2 -> ... -> pn -> start
        cost = path_cost[(start, perm[0])]
        for i in range(len(perm) - 1):
            cost += path_cost[(perm[i], perm[i + 1])]
        cost += path_cost[(perm[-1], start)]

        if cost < min_cost:
            min_cost = cost
            best_order = perm

    return best_order, min_cost


def build_full_path(start, order, path_sequence):
    """构建完整路径序列"""
    full_path = [start]
    current = start

    for next_point in order:
        segment = path_sequence[(current, next_point)][1:]  # 跳过重复节点
        full_path.extend(segment)
        current = next_point

    # 回到起点
    segment = path_sequence[(current, start)][1:]
    full_path.extend(segment)

    return full_path


# 主程序
if __name__ == "__main__":
    # 参数配置
    start_point = 'A'
    garbage_points = ['B', 'C', 'D']

    # 初始化图
    graph = setup_graph()
    graph.generate_nodes()

    # 预计算路径
    all_points = [start_point] + garbage_points
    cost_matrix, path_matrix = calculate_paths(graph, all_points)

    # 寻找最优路径
    best_order, min_cost = find_optimal_route(start_point, garbage_points, cost_matrix)

    # 构建完整路径
    if best_order:
        full_path = build_full_path(start_point, best_order, path_matrix)
        print(f"Optimal Route: {' → '.join(full_path)}")
        print(f"Total Distance: {min_cost}")
    else:
        print("No valid path found!")

# 输入输出示例：
"""
输入：
- 车库/起点: A
- 必须访问的垃圾点: B, C, D
- 图结构:
  A <-> B (双向，成本1)
  B -> C (单向，成本2)
  C -> D (单向，成本3)
  D <-> A (双向，成本4)
  B <-> D (双向，成本5)

输出：
Optimal Route: A → B → C → D → A
Total Distance: 10
"""