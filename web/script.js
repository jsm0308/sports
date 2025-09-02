// 새로운 Client ID와 Secret을 변수에 저장
const CLIENT_ID = '27nkfb9obp';
const CLIENT_SECRET = 'MBTYTEMRvKzGxvFE6myaoXXjN0tdpsb7xwFTA3U3';

// ------------------------------------------------------------------
// [새 기능] 지도 API 인증 실패 시 경고창을 띄우는 함수
// 이 코드를 추가하면 인증 실패 원인을 더 쉽게 파악할 수 있습니다.
window.navermap_authFailure = function () {
    alert("네이버 지도 인증에 실패했습니다. ncpKeyId와 웹 서비스 URL 설정을 확인해주세요.");
};
// ------------------------------------------------------------------


let currentPolyline = null;

// 1. 지도 생성
const map = new naver.maps.Map('map', {
    center: new naver.maps.LatLng(37.5172, 127.0473),
    zoom: 13
});

// 2. 길찾기 함수 (변경 없음)
function findRoute(option) {
    const start = '127.0276,37.4979'; // 강남역
    const goal = '126.9780,37.5665';  // 서울시청
    const url = `https://maps.apigw.ntruss.com/map-direction/v1/driving?start=${start}&goal=${goal}&option=${option}`;

    fetch(url, {
        method: "GET",
        headers: {
            "X-NCP-APIGW-API-KEY-ID": CLIENT_ID,
            "X-NCP-APIGW-API-KEY": CLIENT_SECRET,
        },
    })
    .then(response => response.json())
    .then(data => {
        if (data.route && data.route[option]) {
            const path = data.route[option][0].path;
            drawPath(path);
        } else {
            console.error("경로 탐색 결과가 없습니다:", data);
            alert("경로를 찾을 수 없습니다. API Key나 설정을 확인해주세요.");
        }
    })
    .catch(error => {
        console.error("API 호출 중 오류 발생:", error);
        alert("길찾기 중 오류가 발생했습니다.");
    });
}

// 3. 경로를 지도에 그리는 함수 (변경 없음)
function drawPath(path) {
    if (currentPolyline) {
        currentPolyline.setMap(null);
    }
    const newPath = path.map(point => new naver.maps.LatLng(point[1], point[0]));
    currentPolyline = new naver.maps.Polyline({
        path: newPath,
        strokeColor: '#e74c3c',
        strokeOpacity: 0.8,
        strokeWeight: 6,
        map: map
    });
    map.panToBounds(currentPolyline.getBounds());
}