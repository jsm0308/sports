
import networkx as nx
import random
import math

# --- 1. 현실적인 교통 네트워크 생성 ---
def create_realistic_transport_graph():
    """
    환승과 여러 경로가 포함된, 더 현실적인 교통 네트워크 그래프를 생성합니다.
    노드 이름 규칙: '종류_이름_노선(선택)'
    """
    G = nx.MultiDiGraph() # 방향성이 있고, 두 노드 사이에 여러 엣지를 허용하는 그래프

    # 각 노드에 가상의 좌표(x, y)를 추가하여, A*의 휴리스틱(최적화)에 사용
    G.add_node("stadium_gate1", pos=(0, 0))
    G.add_node("subway_sports_complex_line2", pos=(1, 1))
    G.add_node("subway_sports_complex_line9", pos=(1, 0))
    G.add_node("bus_stop_A", pos=(0, 2))
    G.add_node("subway_samseong", pos=(5, 1))
    G.add_node("bus_stop_B", pos=(5, 2))
    G.add_node("home", pos=(10, 1))

    # 엣지 추가 (이동 경로)
    # 1. 도보 경로
    G.add_edge("stadium_gate1", "subway_sports_complex_line2", type='walk', time=8)
    G.add_edge("stadium_gate1", "bus_stop_A", type='walk', time=12)
    
    # 2. 지하철 경로
    G.add_edge("subway_sports_complex_line2", "subway_samseong", type='subway', time=5)
    
    # 3. 버스 경로
    G.add_edge("bus_stop_A", "bus_stop_B", type='bus', time=10)
    
    # 4. 환승 경로 (가장 중요!)
    G.add_edge("subway_samseong", "bus_stop_B", type='walk', time=5) # 삼성역에서 B정류장으로 환승
    
    # 5. 최종 귀가 경로
    G.add_edge("subway_samseong", "home", type='walk', time=15)
    G.add_edge("bus_stop_B", "home", type='walk', time=10)
    
    return G

# --- 2. 실시간 데이터 조회 (API 호출 시뮬레이션) ---
def get_realtime_bus_wait_time(stop_id):
    """실제로는 API를 호출하겠지만, 여기서는 랜덤값으로 대기 시간을 시뮬레이션합니다."""
    # print(f"DEBUG: {stop_id}의 실시간 버스 대기 시간 조회 중...")
    return random.randint(1, 10) # 1분 ~ 10분 사이의 대기 시간 반환

# --- 3. 최적 경로 탐색 (업그레이드) ---
def find_optimal_path_advanced(graph, start, end, mode, predicted_congestion=0):
    """업그레이드된 A* 알고리즘으로, 실시간 데이터와 환승을 고려하여 경로를 탐색합니다."""

    def cost_function(u, v, d):
        """A* 알고리즘이 사용할 비용 계산 함수 (더 정교해짐)"""
        edge_data = d[0] # MultiDiGraph는 엣지 데이터가 딕셔너리 안에 있음
        edge_time = edge_data.get('time', 0)
        edge_type = edge_data.get('type', 'walk')
        
        total_cost = edge_time
        
        # 실시간 버스 대기 시간 반영
        if edge_type == 'bus':
            wait_time = get_realtime_bus_wait_time(u) # u: 출발 정류장 이름
            total_cost += wait_time

        # '쾌적한 경로' 모드일 때 혼잡도 페널티 적용
        if mode == 'comfortable':
            if edge_type in ['subway', 'bus']:
                congestion_penalty = edge_time * (predicted_congestion / 100) * 1.5
                total_cost += congestion_penalty
        
        return total_cost
    
    # A* 알고리즘의 효율을 높이기 위한 휴리스틱 함수 (두 지점 간의 직선 거리를 추정)
    def heuristic(u, v):
        pos_u = graph.nodes[u].get('pos', (0,0))
        pos_v = graph.nodes[v].get('pos', (0,0))
        # 직선 거리를 기반으로 최소 예상 시간을 추정 (1 unit = 1분으로 가정)
        return math.sqrt((pos_u[0] - pos_v[0])**2 + (pos_u[1] - pos_v[1])**2)

    try:
        path = nx.astar_path(graph, source=start, target=end, weight=cost_function, heuristic=heuristic)
        return path
    except nx.NetworkXNoPath:
        return None

# --- 이 파일을 직접 실행할 경우 테스트 진행 ---
if __name__ == '__main__':
    G = create_realistic_transport_graph()
    start_node, end_node = "stadium_gate1", "home"
    
    # 가상의 예측 혼잡도를 180%로 매우 높게 설정
    mock_congestion = 180
    
    print(f"가상 예측 혼잡도: {mock_congestion}%")
    print("-" * 30)

    # 1. 빠른 경로 모드
    fast_path = find_optimal_path_advanced(G, start_node, end_node, 'fast', mock_congestion)
    print(f"🟢 '빠른 경로' 모드 추천:")
    print(f"   - 경로: {fast_path}")
    
    print("-" * 30)
    
    # 2. 쾌적한 경로 모드
    comfortable_path = find_optimal_path_advanced(G, start_node, end_node, 'comfortable', mock_congestion)
    print(f"🟡 '쾌적한 경로' 모드 추천:")
    print(f"   - 경로: