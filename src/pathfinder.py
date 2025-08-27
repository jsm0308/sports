# app/pathfinder.py

import networkx as nx

# --- 1. 교통 네트워크 생성 ---
def create_transport_graph():
    """테스트용 교통 네트워크 그래프를 생성합니다."""
    G = nx.Graph()
    G.add_edge("경기장", "A역", type='walk', time=10)
    G.add_edge("경기장", "C정류장", type='walk', time=15)
    G.add_edge("A역", "B역", type='subway', time=5)
    G.add_edge("C정류장", "B역", type='bus', time=8)
    G.add_edge("B역", "집", type='subway', time=20)
    return G

# --- 2. 최적 경로 탐색 ---
def find_optimal_path(graph, start, end, mode, predicted_congestion=0):
    """A* 알고리즘을 사용하여 최적 경로를 탐색합니다."""
    
    def cost_function(u, v, d):
        """A* 알고리즘이 사용할 비용 계산 함수."""
        edge_time = d.get('time', 0)
        
        if mode == 'fast':
            return edge_time
            
        elif mode == 'comfortable':
            congestion_penalty = 0
            if d.get('type') in ['subway', 'bus']:
                congestion_penalty = edge_time * (predicted_congestion / 100) * 1.5
            return edge_time + congestion_penalty
            
    try:
        path = nx.astar_path(graph, source=start, target=end, weight=cost_function)
        return path
    except nx.NetworkXNoPath:
        return None

# --- 이 파일을 직접 실행할 경우 테스트 진행 ---
if __name__ == '__main__':
    graph = create_transport_graph()
    mock_congestion = 150 
    
    print(f"가상 예측 혼잡도: {mock_congestion}%")
    
    fast_path = find_optimal_path(graph, "경기장", "집", mode='fast', predicted_congestion=mock_congestion)
    print(f"🟢 빠른 경로: {fast_path}")
    
    comfortable_path = find_optimal_path(graph, "경기장", "집", mode='comfortable', predicted_congestion=mock_congestion)
    print(f"🟡 쾌적한 경로: {comfortable_path}")