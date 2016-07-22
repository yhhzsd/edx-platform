(function(require) {
    require(['edx-ui-toolkit/js/utils/html-utils'], function(HtmlUtils) {
        $(function() {
            HtmlUtils.setHtml(".about-container", $("#about-content").html().toString())
            addSlider();
        });

        $(window).resize(function(){
            addSlider();
        });

        function addSlider(){
            var isMobileResolution = $(window).width() < 768,
                sliderExists = $(".about-list").hasClass("slick-slider");

            $(".about-list").toggleClass("slidable", isMobileResolution);

            if (isMobileResolution) {    //Second condition will avoid the multiple calls from resize
              if (!sliderExists) {
                $(".about-list").find(".about-list-item").removeClass('col col-4');
                $(".slidable").slick({
                  nextArrow: '<i class="fa fa-angle-right"></i>',
                  prevArrow: '<i class="fa fa-angle-left"></i>',
                });
              }
            } else {
                HtmlUtils.setHtml(".about-container", $("#about-content").html().toString())
            }
         }
    });
}).call(this, require || RequireJS.require);

