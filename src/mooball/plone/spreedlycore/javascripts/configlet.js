/******************************************************************************
 *
 * jQuery functions for the mooball.plone.spreedlycore viewlet and form.
 *
 ******************************************************************************/
(function ($) {
    /* Update settings */
    $.updateSettings = function () {
        var spreedly_login = $("#content").hasClass("spreedly_login");
        var spreedly_secret = $("#content").hasClass("spreedly_secret");
        var form = $("form#SpreedlyLoginSettingsForm");
        
        /* If all credentials filled in, show Gateway Drop Down, or disable */
        if ((spreedly_login === true) && (spreedly_secret == true)) {
            form.addClass('unclickable');
            var field = form.find("select");
            field.removeAttr('disabled');
        }
        else {
            form.removeClass('unclickable');
            var field = form.find("select");
            field.attr('disabled', 'disabled');
        }
    };
    
    /**************************************************************************
     * Window Load Function: Executes when complete page is fully loaded,
     * including all frames,
     **************************************************************************/
    $(window).load(function () {
        // Update settings on page load
        $.updateSettings();
    });

    //#JSCOVERAGE_ENDIF

}(jQuery));
