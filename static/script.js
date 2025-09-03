// --- 지도 초기화 ---
const mapDiv = document.getElementById("map");
const map = new naver.maps.Map(mapDiv, {
    center: new naver.maps.LatLng(37.5113, 127.0982),
    zoom: 15,
});

// --- 전역 변수 ---
let currentPolyline = null; // 현재 지도에 그려진 경로
let mockRouteData = null; // 가상 경로 데이터 저장

// --- UI 요소 ---
const submitBtn = document.querySelector('.submit-btn');
const resultsPanel = document.getElementById('results-panel');
const tabs = document.querySelectorAll('.tab-btn');

// --- 가상 API 호출 함수 (백엔드 연동 시 이 부분을 실제 fetch로 교체) ---
async function fetchRouteData(start, end) {
    console.log(`경로 탐색 요청: ${start} -> ${end}`);
    
    // 가상 데이터 생성 (실제 API 응답 형식과 유사하게 구성)
    const mockData = {
        fastest: { // 최단 시간 경로
            totalTime: 35,
            walkTime: 10,
            transferCount: 1,
            path: [
                [127.0982, 37.5113], [127.099, 37.5105], [127.100, 37.5090],
                [127.101, 37.5080], [127.098, 37.5060], [127.095, 37.5040],
                [127.093, 37.5030], [127.090, 37.5015], [127.085, 37.4990],
                [127.080, 37.4980], [127.075, 37.4975], [127.028, 37.4982] // 강남역 근처
            ]
        },
        walk: { // 최소 도보 경로
            totalTime: 45,
            walkTime: 5,
            transferCount: 2,
            path: [
                [127.0982, 37.5113], [127.100, 37.5120], [127.102, 37.5110],
                [127.103, 37.5100], [127.100, 37.5080], [127.095, 37.5050],
                [127.090, 37.5020], [127.085, 37.5000], [127.080, 37.4990],
                [127.070, 37.4985], [127.028, 37.4982] // 강남역 근처
            ]
        }
    };

    // 네트워크 지연 시간 시뮬레이션 (0.5초)
    return new Promise(resolve => {
        setTimeout(() => {
            resolve(mockData);
        }, 500);
    });
}

// --- 지도에 경로 그리는 함수 ---
function drawPolyline(path) {
    // 기존에 그려진 경로가 있다면 삭제
    if (currentPolyline) {
        currentPolyline.setMap(null);
    }

    currentPolyline = new naver.maps.Polyline({
        path: path.map(p => new naver.maps.LatLng(p[1], p[0])), // [lng, lat] -> LatLng 객체로 변환
        strokeColor: '#e74c3c',
        strokeOpacity: 0.8,
        strokeWeight: 6,
        map: map
    });
    
    // 경로가 보이도록 지도 경계 조정
    map.fitBounds(currentPolyline.getBounds());
}

// --- 결과 패널 업데이트 함수 ---
function updateResultPanel(data) {
    document.getElementById('total-time').textContent = data.totalTime;
    document.getElementById('walk-time').textContent = data.walkTime;
    document.getElementById('transfer-count').textContent = data.transferCount;
    resultsPanel.classList.add('show');
}

// --- 이벤트 리스너 ---

// 경로 탐색 버튼 클릭 이벤트
submitBtn.addEventListener('click', async () => {
    const startInput = document.getElementById('start').value;
    const destinationInput = document.getElementById('destination').value;

    // API 호출 및 데이터 저장
    mockRouteData = await fetchRouteData(startInput, destinationInput);
    
    // 기본으로 '최단 시간' 경로를 보여줌
    const defaultPathType = 'fastest';
    document.querySelector('.tab-btn.active').classList.remove('active');
    document.querySelector(`.tab-btn[data-path="${defaultPathType}"]`).classList.add('active');
    
    drawPolyline(mockRouteData[defaultPathType].path);
    updateResultPanel(mockRouteData[defaultPathType]);
});

// 결과 패널 탭 클릭 이벤트
tabs.forEach(tab => {
    tab.addEventListener('click', () => {
        if (!mockRouteData) return; // 경로 데이터가 없으면 아무것도 안 함

        // 모든 탭에서 active 클래스 제거 후 클릭된 탭에 추가
        tabs.forEach(t => t.classList.remove('active'));
        tab.classList.add('active');

        const pathType = tab.dataset.path;
        const routeInfo = mockRouteData[pathType];
        
        drawPolyline(routeInfo.path);
        updateResultPanel(routeInfo);
    });
});