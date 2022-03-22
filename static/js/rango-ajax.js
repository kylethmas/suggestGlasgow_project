
$(document).ready(function() {
	$('#like_btn').click(function() {
		var placeIdVar;
		placeIdVar = $(this).attr('data-placeid');
		
		$.get('/suggestGlasgow/LikePlace/',
			{'place_id': placeIdVar},
			function(data) {
				$('#like_count').html(data);
				$('#like_btn').hide();
				//maybe show the image?
			})
	});
});