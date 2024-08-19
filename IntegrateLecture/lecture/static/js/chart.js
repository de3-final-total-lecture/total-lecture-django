document.addEventListener('DOMContentLoaded', function() {
    const ctx = document.getElementById('sentimentChart').getContext('2d');
    new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: ['긍정적', '부정적', '중립적'],
            datasets: [{
                data: [positivePercentage, negativePercentage, neutralPercentage],
                backgroundColor: ['#4CAF50', '#F44336', '#FFC107'],
                hoverBackgroundColor: ['#66BB6A', '#E57373', '#FFD54F']
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    position: 'top',
                },
                tooltip: {
                    callbacks: {
                        label: function(tooltipItem) {
                            return tooltipItem.label + ': ' + tooltipItem.raw + '%';
                        }
                    }
                }
            }
        }
    });

    // 평균 감정 바 설정
    const avgSentimentElement = document.querySelector('.avg-sentiment');
    
    if (avgSentiment >= 0 && avgSentiment <= 1) {
        avgSentimentElement.style.width = `${avgSentiment * 100}%`;
        avgSentimentElement.textContent = `${(avgSentiment * 100).toFixed(2)}%`;
    } else {
        console.error("Average sentiment value is out of bounds");
    }
});


document.addEventListener('DOMContentLoaded', function() {
    const ctx = document.getElementById('priceHistoryChart').getContext('2d');


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