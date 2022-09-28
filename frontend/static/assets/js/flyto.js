/*!
 * jQuery lightweight Fly to
 * Author: @ElmahdiMahmoud
 * Licensed under the MIT license
 */

// self-invoking
;(function ($, window, document, undefined) {
    $.fn.flyto = function ( options ) {
        
    // Establish default settings
        
        var settings = $.extend({
            item      : '.flyto-item',
            target    : '.flyto-target',
            button    : '.flyto-btn',
            shake     : false
        }, options);
        
        
        return this.each(function () {
            var 
                $this    = $(this),
                flybtn   = $this.find(settings.button),
                target   = $(settings.target),
                itemList = $this.find(settings.item);
            
        flybtn.on('click', function () {
            if ($(this).hasClass("added")) {
                $(this).removeClass("added");
                return null;
            }
            else {
                $(this).addClass("added");
            }
            
            
            var _this = $(this),
                eltoDrag = _this.parent().find("img.pro-card-img").eq(0);
        if (eltoDrag) {
            var imgclone = eltoDrag.clone()
                .offset({
                top: eltoDrag.offset().top,
                left: eltoDrag.offset().left
            })
                .css({
                    'opacity': '0.5',
                    'position': 'absolute',
                    // 'height': 150,
                    'width': 150,
                    'z-index': '100000'
            })
                .appendTo($('body'))
                .animate({
                    'top': target.offset().top + 10,
                    'left': target.offset().left - 30,
                    // 'height': 75,
                    'width': 75
            }, 1000, 'easeInOutExpo');
            
            if (settings.shake) {
            setTimeout(function () {
                target.effect("shake", {
                    times: 2
                }, 200);
            }, 1500);
            }

    
            imgclone.animate({
                'width': 0,
                'height': 0,
                'left': target.offset().left + 5,
            }, function () {
                $(this).detach()
            });
        }
        });
        });
    }
})(jQuery, window, document);