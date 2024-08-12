document.addEventListener('DOMContentLoaded', function() {
    const ctx = document.getElementById('priceHistoryChart').getContext('2d');
    console.log("hihihi")

    new Chart(ctx, {
        type: 'line',
        data: {
            labels: priceHistoryDate,
            datasets: [{
                label: 'Price',
                data: priceHistory,
                borderColor: 'rgba(1, 55, 255, 1)',
                backgroundColor: 'rgba(75, 192, 192, 0.5)',
                borderWidth: 1,
                pointRadius: 5,
                pointHoverRadius: 7 
            }]
        },
        options: {
            scales: {
                y: {
                    beginAtZero: true
                }
            },
            interaction: {
                mode: 'nearest', // 가장 가까운 포인트를 찾음
                axis: 'x', // x축 기준으로 동작
                intersect: false // x축의 모든 포인트에 대해 마우스 오버 가능
            }
        }
    });
});

// window.onload = function() {
//     // JSON 데이터를 파싱하여 JavaScript 변수로 사용
//     console.log("loaded!")

//     const ctx = document.getElementById('priceHistoryChart').getContext('2d');
//     const priceChart = new Chart(ctx, {
//         type: 'line',
//         data: {
//             labels: priceHistoryDate,  // x축 데이터 (날짜)
//             datasets: [{
//                 label: 'Price',
//                 data: priceHistory,  // y축 데이터 (가격)
//                 borderColor: 'rgba(75, 192, 192, 1)',
//                 backgroundColor: 'rgba(75, 192, 192, 0.2)',
//                 borderWidth: 1
//             }]
//         },
//         options: {
//             scales: {
//                 x: {
//                     type: 'time',
//                     time: {
//                         unit: 'day',  // x축 단위를 'day'로 설정 (시간 단위도 가능)
//                         tooltipFormat: 'll HH:mm'  // 툴팁에 표시할 포맷
//                     },
//                     title: {
//                         display: true,
//                         text: 'Date'
//                     }
//                 },
//                 y: {
//                     beginAtZero: true,
//                     title: {
//                         display: true,
//                         text: 'Price'
//                     }
//                 }
//             }
//         }
//     });
// };