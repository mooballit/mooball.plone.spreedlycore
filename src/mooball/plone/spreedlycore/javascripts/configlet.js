/******************************************************************************
 *
 * jQuery functions for the mooball.plone.spreedlycore viewlet and form.
 *
 ******************************************************************************/
(function ($) {
    // This unnamed function allows us to use $ inside of a block of code
    // without permanently overwriting $.
    // http://docs.jquery.com/Using_jQuery_with_Other_Libraries
    
    /* Disable a control panel setting */
    $.disableSettings = function (settings) {
        $.each(settings, function (intIndex, setting) {
            setting.addClass('unclickable');
            var setting_field = $(setting).find("input,select");
            setting_field.attr('disabled', 'disabled');
        });          
    };
    
    /* Enable a control panel setting */
    $.enableSettings = function (settings) {
        $.each(settings, function (intIndex, setting) {
            setting.removeClass('unclickable');
            var setting_field = $(setting).find("input,select");
            setting_field.removeAttr('disabled');
        });    
    };
    
    /* Update settings */
    $.updateSettings = function () {
        var default_spreedly_gateway = $("#content").hasClass("default_spreedly_gateway");
        
        /* If commenting is globally disabled, disable all settings. */
        if (globally_enabled === true) {
            $.enableSettings([
                $('#form-widgets-default_spreedly_gateway')
            ]);
        }
        else {
            $.disableSettings([
                $('#form-widgets-default_spreedly_gateway')
            ]);
        }
    };
    //#JSCOVERAGE_IF 0
    
    /**************************************************************************
     * Window Load Function: Executes when complete page is fully loaded,
     * including all frames,
     **************************************************************************/
    $(window).load(function () {
    
        // Update settings on page load
        $.updateSettings();
        
        // Set #content class and update settings afterwards
        $("input,select").live("change", function (e) {
            var id = $(this).attr("id");
            if (id === "form-widgets-globally_enabled-0") {    
                if ($(this).attr("checked") === true) {
                    $("#content").addClass("globally_enabled");
                }
                else {
                    $("#content").removeClass("globally_enabled");
                }
                $.updateSettings();
            }
        });
        
        /**********************************************************************
         * Remove the disabled attribute from all form elements before 
         * submitting the form. Otherwise the z3c.form will raise errors on
         * the required attributes.
         **********************************************************************/
        $("form#SpreedlyLoginSettingsEditForm").bind("submit", function (e) {
            $(this).find("input,select").removeAttr('disabled');
			$(this).submit();
        });
        
    });

    //#JSCOVERAGE_ENDIF

}(jQuery));
