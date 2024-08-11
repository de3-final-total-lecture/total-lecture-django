<script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>

$(document).ready(function(){
    $('.lecture_item').on('click', function(){
        const lecture_id = $(this).data('lecture_id'); // Click한 Lecture의 Id를 가져오기
        const user_id = {{ request.user.pk }};

        $.ajax({
            url: `{% url 'user_click' %}`,
            method: 'POST',
            data: {
                'lecture_id': lecture_id,
                'user_id': user_id,
                'csrfmiddlewaretoken': '{{ csrf_token }}'
            },
            success: function(response) {
                alert(response.message);  // 성공 메시지
            },
            error: function(xhr, status, error) {
                console.error(error);
            }
        });
    });
});