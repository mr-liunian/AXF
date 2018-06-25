$(function () {
    initTopSwiper();
    initTopMenu();
})

function initTopSwiper() {
    var swiper = new Swiper('#topSwiper',{
        pagination:'.swiper-pagination',
        autoplay : 3000,
    })
}
function initTopMenu() {
    var swiper = new Swiper('#swiperMenu',{
        slidesPerView:3

    })

}