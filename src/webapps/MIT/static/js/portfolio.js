function getPortfolioInfo() {
    var playerid = $("#gamePlayerID").val()
    var gameid = $("#gameID").val()
    // validation check
    if (($.isNumeric(playerid) == false)||($.isNumeric(gameid) == false)) {
      return
    }

    $.get("/get-share-info/" + gameid + "/" + playerid)
        .done(function(data) {
            var name = data.name
            var percent = data.percent
            stockInfo(name, percent)
        });
}

function stockInfo(name, percent) {
    var myChart = echarts.init(document.getElementById('graph'));
    var data_list = []
    for (var i = 0; i < percent.length; i++) {
        var map = {
            name: name[i],
            type: 'bar',
            stack: '总量',
            label: {
                normal: {
                    show: true,
                    position: 'insideRight'
                }
            },
            data: [percent[i]]
        }
        data_list.push(map)
    }
    var option = {
        title: {
            text: 'PORTFOLIO ALLOCATION',
            textStyle: {
                fontSize: 10,
                color: 'grey'
            },
            padding: [0, 47, 10, 47]

        },
        tooltip: {
            trigger: 'axis',
            axisPointer: {
                type: 'shadow'
            }
        },
        legend: {
            data: name,
            bottom: true,
            left: 'left',
            padding: [0, 47, 10, 47]
        },
        grid: {
            left: '3%',
            right: '2%',
            bottom: '80%',
            containLabel: true
        },
        xAxis: {
            type: 'value',
            show: false
        },
        yAxis: {
            type: 'category',
            data: ['    '],
            show: false
        },
        series: data_list

    };
    myChart.setOption(option);
}


$(document).ready(function() {
    // Initialize the plugin
    getPortfolioInfo();
    $('#cash-remaining-icon').tooltip({title: "This is the amount of cash the investor has available to make a trade"});
    // window.setInterval(getPortfolioInfo, 6000);
    $('#short-reserve-icon').tooltip({title: "This is the amount of money required to close short postion in your amount"});

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

});
