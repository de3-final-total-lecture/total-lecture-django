document.addEventListener('DOMContentLoaded', function() {
    const ctx = document.getElementById('sentimentChart').getContext('2d');
    new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: ['중립적', '부정적', '긍정적'],
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
