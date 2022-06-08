$(document).ready(function() {
    let ctx = document.querySelector('#loginActivityChart');
    Chart.defaults.color = "#696969";
    let revChart = new Chart(ctx, {
        type: "line",
        data: {
            labels: [], // Dates
            datasets: [
                {
                    label: "Success",
                    borderColor: "#0F9D58",
                    borderWidth: "3",
                    backgroundColor: "#0f9d5833",
                    data: [], // success_attempts_date
                },
                {
                    label: "Failed",
                    borderColor: "#DB4437",
                    borderWidth: "3",
                    backgroundColor: "#db443733",
                    data: [], // failed_attempts_date
                },
            ]
        },
        options: {
            responsive: true,
            tooltips: {
                intersect: false,
                node: "index",
            }
        }
    });

    var fetchLDURLs = $('.graph-select').data('fetch-login-details-url');
    $('#id_request_month').change(function() {
        var reqMonth = $('#id_request_month').val();
        reqMonth = parseInt(reqMonth);
        if (reqMonth > 0 && reqMonth < 13) {
            $.ajax({
                type: "POST",
                url: fetchLDURLs,
                data: {
                    'csrfmiddlewaretoken':$('input[name=csrfmiddlewaretoken]').val(),
                    'request_month': reqMonth,
                },
                success: function (data) {
                    // Iterate and push dates to labels
                    // clear the labels and data
                    revChart.data.labels = [];
                    for (var i = 0; i < data['get_dates'].length; i++) {
                        revChart.data.labels.push(data['get_dates'][i]);
                    }
    
                    revChart.data.datasets[0].data = [];
                    for(var i = 0; i < data['success_attempts_date'].length; i++) {
                        revChart.data.datasets[0].data.push(data['success_attempts_date'][i]);
                    }
    
                    revChart.data.datasets[1].data = [];
                    for(var i = 0; i < data['failed_attempts_date'].length; i++) {
                        revChart.data.datasets[1].data.push(data['failed_attempts_date'][i]);
                    }
                    
                    // re-render the chart
                    revChart.update();
                },
                error: function (data) {
                    toastr.error("Something went wrong!");
                }
            });
        }
    });

    $('input[name="checkbox_backup_code"]').click(function(){
        var status_2fa_url = $(this).data('href');
        if($(this).prop("checked") == true){
            $.ajax({
                url: status_2fa_url,
                method: "GET",
                data: {},
                success: function(data) {
                    window.location.reload();
                }, error: function(error) {
                    console.log('Here2');
                }
            });
        }
        else if($(this).prop("checked") == false){
            $.ajax({
                url: status_2fa_url,
                method: "GET",
                data: {},
                success: function(data) {
                    window.location.reload();
                }, error: function(error) {
                    console.log('Here4');
                }
            });
        }
    });

    $(".show-details-login-info").slice(0, 3).show();
    if ($(".show-details-login-info:hidden").length != 0) {
      $("#loadMore").show();
    }   
    $("#loadMore").on('click', function (e) {
      e.preventDefault();
      $(".show-details-login-info:hidden").slice(0, 6).slideDown();
      if ($(".show-details-login-info:hidden").length == 0) {
        $("#loadMore").fadeOut('slow');
      }
      $('html,body').animate({
        scrollTop: $(this).offset().top
      }, 100);
    });
});