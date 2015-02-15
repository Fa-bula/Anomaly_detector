$(document).ready(function() {
    $("select[id=select_method]").change(function () {
	$('div[id*=desc-]').parent().addClass('hide')
	$("#desc-" + $("select#select_method").val()).parent().removeClass('hide');
    }).change();
});
