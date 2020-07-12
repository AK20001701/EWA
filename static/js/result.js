function drawPie(max_result, user_result) {
    var ctx = document.getElementById('myChart').getContext('2d');
    var myChart = new Chart(ctx, {
        type: 'pie',
        data: {
            datasets: [{
                // labels: ['Правильно', 'Неправильно'],
                data: [max_result - user_result, user_result],
                backgroundColor: [
                    'rgba(255, 99, 132, 0.2)',
                    'rgb(58,232,46, 0.2)'
                ],
                borderColor: [
                    'rgba(255, 99, 132, 1)',
                    'rgb(58,232,46, 1)',
                ],
                borderWidth: 1
            }]
        }
    });
}