$("#back_manageadmission").click(function () {
    var backTomanageadmission = $(this).data('back-to-manage-admission');
    $("#back_manageadmission").prop("disabled", true);
    setTimeout(function () {
        $("#back_manageadmission").prop("disabled", false);
    }, 5000);
    window.location.href = backTomanageadmission;
});