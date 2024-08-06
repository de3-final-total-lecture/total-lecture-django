$(document).ready(function() {

    $('.tab-button').click(function () {
        var target = $(this).data('target');
        var targetOffset = $('#' + target).offset().top - $('.tab-container').height();

        $('html, body').animate({
            scrollTop: targetOffset
        }, 500);

        // 클릭된 탭 버튼에 active 클래스 추가
        $('.tab-button').removeClass('active');
        $(this).addClass('active');
    });

    // 스크롤 시 탭 활성 상태 업데이트
    $(window).scroll(function () {
        var scrollPos = $(window).scrollTop();
        $('.tab-button').each(function () {
            var target = $(this).data('target');
            var targetOffset = $('#' + target).offset().top - $('.tab-container').height() - 10;

            if (scrollPos >= targetOffset) {
                $('.tab-button').removeClass('active');
                $(this).addClass('active');
            }
        });
    });

    // what_do_i_learn 구분자 제거
    var whatDoILearn = $('.lecture-whatlearn').data('contents');
    var learns = whatDoILearn.split('|');
    var learn_html = '';
    learns.forEach(function(learn) {
        learn_html += '<div class="item"> # ' + learn + '</div>';
    });
    $('what-do-i-learn-container').html(learn_html);

    // tag 구분자 제거
    var tagData = $('.tags').data('contents');
    var tags = tagData.split('|');
    var tag_html = '';
    tags.forEach(function(tag) {
        tag_html += '<button class="tag-item" data-tag="{{ tag }}">' + '#'+tag + '</button>';
    });
    $('.tags').html(tag_html);

    var rating = parseFloat($('.lecture-rating').data('rating')); // rating 값을 data-attribute에서 가져옴
    $('#rating-stars').html(getStarRatingHtml(rating));

    $('#heart-icon, #sticky-heart-icon, #header-heart-icon').on('click', function() {
        $(this).toggleClass('liked');
        if ($(this).hasClass('liked')) {
            $(this).removeClass('fa-regular fa-heart').addClass('fa-solid fa-heart');
        } else {
            $(this).removeClass('fa-solid fa-heart').addClass('fa-regular fa-heart');
        }
    });

    $('.price').each(function() {
        var price = $(this).text().replace('원', '').trim();
        var formattedPrice = price.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
        $(this).text(formattedPrice + '원');
    });

    $(document).on('click', '.num1', function() {
        var lectureId = $(this).data('lectureid');
        var lectureURL = base62Decode(lectureId);

        window.location.href = lectureURL;
    });

});



function getStarRatingHtml(rating) {
    const fullStar = '<i class="fa-solid fa-star"></i>';
    const halfStar = '<i class="fa-regular fa-star-half-stroke"></i>';
    const emptyStar = '<i class="fa-regular fa-star"></i>';
    
    let starsHtml = '';
    let fullStars = Math.floor(rating);
    let hasHalfStar = (rating % 1) >= 0.5;

    for (let i = 0; i < fullStars; i++) {
        starsHtml += fullStar+' ';
    }

    if (hasHalfStar) {
        starsHtml += halfStar+' ';
    }

    const totalStars = 5;
    const remainingStars = totalStars - fullStars - (hasHalfStar ? 1 : 0);
    for (let i = 0; i < remainingStars; i++) {
        starsHtml += emptyStar+' ';
    }

    return starsHtml;
}

