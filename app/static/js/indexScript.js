$('.create-panel .img-size1').hide();
$('.join-panel .img-size2').hide();
$('.create-panel img').hide();
$('.join-panel img').hide();
$('.anon-panel img').hide();

$('#avatar1').bind('change', function() {
	var sizeAv1 = 0;
	var f = this.files[0];
	$('.create-panel .img-size1').hide();
	sizeAv1 = f.size/1024; 
	if(sizeAv1 > 100) {
		sizeAv1 = 0;
		$('.create-panel .img-size1').show();
		$('#avatar1').val('');
	}
	else if(f.type.search("jpeg") == -1 && f.type.search("png") == -1) {
		alert("Only image formats allowed.");
		$('#avatar1').val('');
	}
});

$('#avatar2').bind('change', function() {
	var sizeAv2 = 0;
	var f = this.files[0];
	$('.join-panel .img-size2').hide();
	sizeAv2 = f.size/1024;
	if(sizeAv2 > 100) {
		sizeAv2 = 0;
		$('.join-panel .img-size2').show();
		$('#avatar2').val('');
	}
	else if(f.type.search("jpeg") == -1 && f.type.search("png") ==-1) {
		alert("Only image formats allowed.");
		$('#avatar2').val('');
	}
});

function go(cls) {
	cls = cls + ' img';
	$(cls).show();
}