(function($) {
    $(function() {
        $('[data-jcarousel]').each(function() {
            var el = $(this);
            console.log(el.data())
            el.jcarousel(el.data());
        });

        $('[data-jcarousel-control]').each(function() {
            var el = $(this);
            el.jcarouselControl(el.data());
        });
    });
})(jQuery);
