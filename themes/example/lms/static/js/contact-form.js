(function(require) {
    require(['edx-ui-toolkit/js/utils/html-utils'], function(HtmlUtils) {

        $(function() {
            $("#submit_btn").click(function(e) {
                e.preventDefault();
                var validate_form = validateForm();
                if (validate_form.is_form_validate) {
                    submitForm(validate_form.data);
                }
            });

        });

        var errorMessages = {
            "name": "Please provide your name.",
            "email": "Please provide a valid e-mail.",
            "details": "Please provide message.",
            "subject": "Please provide an inquiry type."
        }

        function submitForm(data) {
            $.post("/submit_feedback", data, function(data, status) {
                $("#success-message-btn").click();
                setTimeout(function() {
                    $("#lean_overlay").trigger("click");
                    $('#contact_form').trigger("reset");
                }, 2000);
            }).fail(function(xhr, status, error) {
                responseData = jQuery.parseJSON(xhr.responseText);
                addErrorDiv(responseData.field);
            });
        }

        function addErrorDiv(id) {
            var errorDiv = HtmlUtils.joinHtml(
                HtmlUtils.HTML("<div class='has-error field-message'><span class='field-message-content'>"),
                gettext(errorMessages[id]),
                HtmlUtils.HTML('</span></div>')
            ).text;
            $("#" + id).addClass("has-error");
            $("#"+id).parent().append(HtmlUtils.template(errorDiv)().toString());
        }

        function removeErrorDiv(id) {
            $("#" + id).removeClass("has-error");
            $($("#" + id).next()).remove();
        }

        function validateForm() {
            var optional_fields = ["user_type"]; //Optional fields array
            var form_values = $("#contact_form").find(":input"),
                i = 0,
                data = new Object(),
                response = {
                    "is_form_validate": true,
                    data: ""
                };

            for (i = 0; i < form_values.length - 2; i++) {
                var value = $(form_values[i]).val(),
                    id = $(form_values[i]).attr("id");
                removeErrorDiv(id);

                if (value && value !== "") {
                    data[id] = value;
                } else {
                    if ($.inArray(id, optional_fields) == -1) {
                        response.is_form_validate = false;
                        addErrorDiv(id);
                    }
                }

            }
            response.data = data;
            return response;
        }


    });
}).call(this, require || RequireJS.require);
