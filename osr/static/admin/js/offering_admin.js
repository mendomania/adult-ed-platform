// CLB levels should only be shown for Language Programs [ESL+FSL]
// Profession should only be shown for the Bridge Training Program
(function($) {
    $(function() {
        var programField = $('#id_program');
        var professionField = $('#offeringprofession_set-group');
        //var requirementsField = $('#id_requirements').parent().parent().parent().parent();
        var clbField = $('#id_clb_01').parent().parent().parent();

        alert("$$$" + programField + "$$$")
        alert("$$$" + programField.find(":selected").text() + "$$$")
        if (programField && programField.find(":selected").text().length > 0) {
            alert(programField.find(":selected").text());
        }

        var curr = programField.val();
        programField.val("");
        programField.trigger("change");
        programField.val(curr);
        programField.trigger("change");
        programField.trigger("change");
        programField.trigger("change");
        programField.trigger("change");
        programField.trigger("change");

        function toggleVerified(value) {
            // Hide CLB and Profession elements
            professionField.hide();          
            clbField.hide();
            //requirementsField.hide();
            if (((value.indexOf("english") >= 0) && (value.indexOf("second") >= 0)) ||
               ((value.indexOf("french") >= 0) && (value.indexOf("second") >= 0))) {
                clbField.show();
            } else if (value.indexOf("bridge training") >= 0) {
                professionField.show();
                //requirementsField.show();
            }
        }

        // Show or hide on load based on previous value of programField
        toggleVerified(programField.find(":selected").text().toLowerCase());

        // Show or hide on change
        programField.change(function() {
            alert("###" + programField.find(":selected").text() + "###")
            alert("###" + programField.val() + "###")
            toggleVerified(programField.find(":selected").text().toLowerCase());
        });
    });
})(django.jQuery);