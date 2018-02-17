    $(document).ready(function() {
        var date_input = $('input[id="date"]'); //our date input has the name "date"
        var container = $('.bootstrap-iso form').length > 0 ? $('.bootstrap-iso form').parent() : "body";
        var date = new Date();
        date.setDate(date.getDate() - 1);
        var options = {
            format: 'mm/dd/yyyy',
            container: container,
            todayHighlight: true,
            autoclose: true,
            startDate: date,
        };

        date_input.datepicker(options);

        $('#short-reserve-icon').tooltip({ title: "Short selling is a trading strategy that seeks to capitalize on an anticipated decline in the price of a security" });
        $('#stop-loss-icon').tooltip({ title: "An order placed with a broker to sell a security when it reaches a certain price. A stop-loss order is designed to limit an investor’s loss on a position in a security." });
        $('#limit-order-icon').tooltip({ title: "A limit order is an order to buy or sell a stock at a specific price or better. A buy limit order can only be executed at the limit price or lower, and a sell limit order can only be executed at the limit price or higher." });
        $('#starting-balance-icon').tooltip({ title: "Input the cash value player will have available in their portfolio." });


        function getCookie(name) {
            var cookieValue = null;
            if (document.cookie && document.cookie != '') {
                var cookies = document.cookie.split(';');
                for (var i = 0; i < cookies.length; i++) {
                    var cookie = jQuery.trim(cookies[i]);
                    // Does this cookie string begin with the name we want?
                    if (cookie.substring(0, name.length + 1) == (name + '=')) {
                        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                        break;
                    }
                }
            }
            return cookieValue;
        }
        var csrftoken = getCookie('csrftoken');
        $.ajaxSetup({
            beforeSend: function(xhr, settings) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        });
    })