import random
import matplotlib.pyplot as plt
import numpy as np
import argparse

class Node:
    def __init__(self, x, y):
        """
        初始化节点对象。

        参数:
        x (float): 节点的 x 坐标。
        y (float): 节点的 y 坐标。
        """
        self.x = x
        self.y = y
        self.cluster_head = False  # 是否是簇头（当前轮次）
        self.cluster_id = None     # 簇头 ID
        self.eligible = True       # 是否有资格成为簇头（一整轮）
        self.energy = 0.5  # 初始能量（焦耳）
        self.dead = False   # 死亡状态标识


def generate_nodes(num_nodes, area_width, area_height):
    """
    生成指定数量的节点。

    参数:
    num_nodes (int): 节点的数量。
    area_width (int): 区域的宽度。
    area_height (int): 区域的高度。

    返回:
    list: 包含 Node 对象的列表，表示节点的坐标。
    """
    nodes = []
    for _ in range(num_nodes):
        x = random.uniform(0, area_width)  # 在 [0, area_width] 范围内随机生成 x 坐标
        y = random.uniform(0, area_height)  # 在 [0, area_height] 范围内随机生成 y 坐标
        # 初始化节点能量
        node = Node(x, y)
        node.energy = 0.5  # 0.5焦耳初始能量
        nodes.append(node)  # 将坐标作为元组添加到列表中
    return nodes


def draw_nodes(nodes, cluster_heads, round_num):
    """
    绘制节点的坐标，并将同一聚类的节点用相同颜色表示，同时连线到簇头。
    死亡节点用灰色叉叉表示。

    参数:
    nodes (list): 包含 Node 对象的列表。
    cluster_heads (list): 包含簇头节点的列表。
    round_num (int): 当前轮次
    """
    # 定义颜色列表
    colors = plt.cm.tab10.colors  # 使用 matplotlib 的 tab10 颜色映射
    
    # 统计节点
    alive_nodes = [n for n in nodes if not n.dead]
    dead_nodes = [n for n in nodes if n.dead]
    
    # 创建新图形
    plt.figure(figsize=(10, 8))
    
    # 输出节点统计信息
    cluster_head_nodes = [n for n in alive_nodes if n.cluster_head]
    normal_nodes = [n for n in alive_nodes if not n.cluster_head]
    
    print(f"绘图详细信息: 总节点={len(nodes)}, 存活节点={len(alive_nodes)} (普通节点={len(normal_nodes)}, 簇头={len(cluster_head_nodes)}), 死亡节点={len(dead_nodes)}")
    
    if len(alive_nodes) + len(dead_nodes) != len(nodes):
        print(f"警告: 节点计数不匹配! 存活({len(alive_nodes)}) + 死亡({len(dead_nodes)}) != 总数({len(nodes)})")
    
    # 绘制死亡节点（所有死亡节点用同一标签）
    if dead_nodes:
        plt.scatter(
            [n.x for n in dead_nodes],
            [n.y for n in dead_nodes],
            color='gray', 
            marker='x',
            s=30,  # 增大标记大小
            alpha=0.7,  # 增加透明度
            label='Dead Nodes'
        )

    # 绘制存活的普通节点并连线到簇头
    drawn_normal_nodes = 0
    for node in nodes:
        if node.dead or node.cluster_head:
            continue
            
        drawn_normal_nodes += 1
        nearest_cluster_head = None
        for cluster_head in cluster_heads:
            if cluster_head.cluster_id == node.cluster_id:
                nearest_cluster_head = cluster_head
                break

        if nearest_cluster_head:
            color = colors[node.cluster_id % len(colors)]  # 根据簇头 ID 选择颜色
            # 绘制节点
            plt.scatter(node.x, node.y, color=color, marker='o', s=20, label=f'Cluster {node.cluster_id}' if not any(n.cluster_id == node.cluster_id for n in nodes[:nodes.index(node)] if not n.dead and not n.cluster_head) else "")
            # 连线到簇头
            plt.plot([node.x, nearest_cluster_head.x], 
                    [node.y, nearest_cluster_head.y], 
                    color=color, linestyle='--', linewidth=0.5)

    # 绘制存活的簇头节点
    drawn_cluster_heads = 0
    for cluster_head in cluster_heads:
        if not cluster_head.dead:  # 仅绘制存活的簇头
            drawn_cluster_heads += 1
            color = colors[cluster_head.cluster_id % len(colors)]  # 根据簇头 ID 选择颜色
            plt.scatter(cluster_head.x, cluster_head.y, 
                      color=color, marker='*', s=120, 
                      edgecolor='black', 
                      label=f'Cluster Head {cluster_head.cluster_id}')
    
    print(f"绘制统计: 绘制了 {drawn_normal_nodes} 个普通节点和 {drawn_cluster_heads} 个簇头")

    # 添加基站位置
    plt.scatter(area_width/2, area_height/2, color='red', marker='^', s=150, label='Base Station')
    
    plt.xlabel('X Coordinate')
    plt.ylabel('Y Coordinate')
    plt.title(f'Round {round_num}: Nodes with Clustering and Dead Nodes')
    
    # 处理图例重复问题
    handles, labels = plt.gca().get_legend_handles_labels()
    by_label = dict(zip(labels, handles))
    plt.legend(by_label.values(), by_label.keys(), loc='upper right')
    
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.show()






def calculate_nearest_cluster_head(node, cluster_heads):
    """
    计算节点最近的簇头。

    参数:
    node (Node): 当前节点。
    cluster_heads (list): 簇头列表。

    返回:
    Node: 最近的簇头。
    """
    min_distance = float('inf')
    nearest_cluster_head = None
    for cluster_head in cluster_heads:
        distance = calculate_distance(node, cluster_head)
        if distance < min_distance:
            min_distance = distance
            nearest_cluster_head = cluster_head
    return nearest_cluster_head


def calculate_distance(node1, node2):
    """
    计算两个节点之间的欧几里得距离。

    参数:
    node1 (Node): 第一个节点。
    node2 (Node): 第二个节点。

    返回:
    float: 两个节点之间的欧几里得距离。
    """
    return np.sqrt((node1.x - node2.x) ** 2 + (node1.y - node2.y) ** 2)


def calculate_cluster_head_probability(k, N, r, eligible):
    """
    计算节点成为簇头的概率。

    参数:
    k (int): 期望的簇头数量。
    N (int): 网络中节点的总数。
    r (int): 当前的轮次。
    eligible (bool): 节点是否有资格成为簇头。

    返回:
    float: 节点成为簇头的概率。
    """
    if eligible:
        mod = r % (N // k)
        denominator = N - k * mod
        if denominator > 0:
            return k / denominator
    return 0.0

def cluster_head_election(nodes, num_cluster_heads, r):
    """
    选举簇头。

    参数:
    nodes (list): 包含 Node 对象的列表。
    """
    # 计算簇头数量
    num_cluster_heads = max(1, num_cluster_heads)
    print(f"第 {r} 轮选举簇头，簇头数量为 {num_cluster_heads}")

    # 首先重置所有节点的簇头状态
    for node in nodes:
        node.cluster_head = False
    
    # 计算每轮每节点概率
    cluster_heads = []
    max_attempts = 100  # 防止无限循环
    attempts = 0
    while len(cluster_heads) < num_cluster_heads and attempts < max_attempts:
        for node in nodes:
            if len(cluster_heads) >= num_cluster_heads:
                break

            if node.cluster_head:
                continue
            
            probability = calculate_cluster_head_probability(num_cluster_heads, len(nodes), r, node.eligible)
            if random.random() < probability:
                node.cluster_head = True
                node.cluster_id = len(cluster_heads)+1
                node.eligible = False
                cluster_heads.append(node)
                print(f"节点 ({node.x:.1f}, {node.y:.1f}) 被选为簇头")
        attempts += 1

    # 如果仍然无法选出足够簇头，强制选择前N个合格节点
    if len(cluster_heads) < num_cluster_heads:
        eligible_nodes = [n for n in nodes if n.eligible]
        needed = num_cluster_heads - len(cluster_heads)
        for node in eligible_nodes[:needed]:
            node.cluster_head = True
            node.cluster_id = len(cluster_heads)+1
            node.eligible = False
            cluster_heads.append(node)
            print(f"强制选择节点 ({node.x:.1f}, {node.y:.1f}) 作为簇头")

    return cluster_heads


def simulate_data_transmission(nodes, cluster_heads, base_station, round_num):
    """
    模拟完整的数据传输过程（包含能量消耗）
    
    参数:
    nodes: 所有节点列表
    cluster_heads: 当前簇头列表
    base_station: 基站节点
    round_num: 当前轮次
    """
    print(f"\n=== 第 {round_num} 轮数据传输开始 ===")
    
    # 调整后的能耗参数（提高能耗）
    E_elec = 100e-9   # 提高电路能耗到100nJ/bit (原50)
    E_fs = 200e-12     # 自由空间模型提高到20pJ/bit/m² (原10)
    E_mp = 0.0026e-12 # 多径衰减模型提高到0.0026pJ/bit/m⁴ (原0.0013)
    E_DA = 100e-9      # 数据聚合能耗提高到10nJ/bit (原5)
    
    data_size = 3000  # 数据包大小
    
    for node in nodes:
        if node.dead:
            continue
            
        if node.cluster_head:
            # 簇头节点能耗 = 接收能耗 + 聚合能耗 + 传输到基站能耗
            received_bits = len(nodes) * data_size
            distance_to_bs = calculate_distance(node, base_station)
            
            # 接收能耗
            energy_rx = E_elec * received_bits
            # 数据聚合能耗
            energy_da = E_DA * received_bits
            # 传输能耗（根据距离选择模型）
            if distance_to_bs < 100:  # 小于100米用自由空间模型
                energy_tx = E_elec * data_size + E_fs * data_size * (distance_to_bs**2)
            else:
                energy_tx = E_elec * data_size + E_mp * data_size * (distance_to_bs**4)
                
            total_energy = energy_rx + energy_da + energy_tx
        else:
            # 普通节点能耗 = 传输到簇头能耗
            nearest_ch = calculate_nearest_cluster_head(node, cluster_heads)
            distance = calculate_distance(node, nearest_ch)
            
            if distance < 100:
                energy_tx = E_elec * data_size + E_fs * data_size * (distance**2)
            else:
                energy_tx = E_elec * data_size + E_mp * data_size * (distance**4)
                
            total_energy = energy_tx
        
        # 更新能量并检查死亡
        node.energy -= total_energy
        if node.energy <= 0:
            node.dead = True
            print(f"节点 ({node.x:.1f}, {node.y:.1f}) 能量耗尽！")


# 示例用法
if __name__ == "__main__":
    # 创建命令行参数解析器
    parser = argparse.ArgumentParser(description='无线传感器网络分簇模拟')
    parser.add_argument('--nodes', type=int, default=100, help='节点数量 (默认: 100)')
    parser.add_argument('--width', type=int, default=100, help='区域宽度 (默认: 100)')
    parser.add_argument('--height', type=int, default=100, help='区域高度 (默认: 100)')
    parser.add_argument('--cluster-percentage', type=float, default=0.05, help='簇头比例 (默认: 0.05)')
    parser.add_argument('--rounds', type=int, default=10, help='总轮次 (默认: 10)')
    
    # 解析命令行参数
    args = parser.parse_args()
    
    # 使用命令行参数
    total_round = args.rounds
    num_nodes = args.nodes
    area_width = args.width
    area_height = args.height
    cluster_head_percentage = args.cluster_percentage

    # 生成坐标
    nodes = generate_nodes(num_nodes, area_width, area_height)
    num_cluster_heads = int(len(nodes) * cluster_head_percentage)

    # 打印参数信息
    print(f"模拟参数:")
    print(f"节点数量: {num_nodes}")
    print(f"区域大小: {area_width}x{area_height}")
    print(f"簇头比例: {cluster_head_percentage}")
    print(f"总轮次: {total_round}")
    print(f"簇头数量: {num_cluster_heads}\n")

    # 打印结果
    print("生成的节点坐标：")
    for idx, node in enumerate(nodes):
        print(f"节点 {idx + 1}: {node.x}, {node.y}")

    # 添加基站（位于区域中心）
    base_station = Node(area_width/2, area_height/2)
    base_station.dead = False  # 基站不会死亡
    
        
    # 模拟轮数
    for r in range(total_round):
        alive_nodes = [n for n in nodes if not n.dead]
        previous_alive_count = len(alive_nodes)  # 记录本轮开始前的存活节点数
        
        if not alive_nodes:
            print("所有节点已死亡，模拟终止")
            break
            
        # 动态计算簇头数量
        current_num_cluster_heads = max(1, int(len(alive_nodes) * cluster_head_percentage))
        
        # 进行簇头选举
        cluster_heads = cluster_head_election(alive_nodes, current_num_cluster_heads, r)

        # 将结点加入对应簇头
        for node in alive_nodes:
            nearest_cluster_head = calculate_nearest_cluster_head(node, cluster_heads)
            node.cluster_id = nearest_cluster_head.cluster_id

        # 模拟数据传输
        simulate_data_transmission(alive_nodes, cluster_heads, base_station, r)
        
        # 统计存活节点
        current_alive_count = sum(1 for n in nodes if not n.dead)
        
        # 修改绘图条件，增加一个选项让用户可以选择是否每轮都绘图
        if current_alive_count < previous_alive_count or r % 10 == 0:  # 每10轮或有节点死亡时绘图
            print(f"生成第 {r} 轮可视化...")
            draw_nodes(nodes, cluster_heads, r)  # 传入当前轮次
        else:
            print(f"第 {r} 轮跳过绘图")

        # 更新每个节点的 eligible 状态
        if r % (len(alive_nodes) // current_num_cluster_heads) == 0:
            for node in alive_nodes:
                node.eligible = True

        # 清空每个节点的簇头 ID
        for node in alive_nodes:
            node.cluster_id = None

        # 统计存活节点
        alive_count = sum(1 for n in nodes if not n.dead)
        print(f"存活节点数: {alive_count}/{num_nodes}")
        if alive_count > 0:
            print(f"平均剩余能量: {sum(n.energy for n in nodes if not n.dead)/alive_count:.2e} J")
        else:
            print("所有节点已死亡，无法计算平均能量")

    
    
    


