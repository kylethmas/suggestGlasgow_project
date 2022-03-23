
$(document).ready(function() {
	$('#like_btn').click(function() {
		var placeIdVar;
		placeIdVar = $(this).attr('data-placeid');
		
		$.get('/suggestGlasgow/LikePlace/',
			{'place_id': placeIdVar},
			function(data) {
				$('#like_count').html(data);
				$('#like_btn').hide();
				$('#dislike_btn').hide();
				//maybe show the image?
			})
	});
});


$(document).ready(function() {
	$('#dislike_btn').click(function() {
		var placeIdVar;
		placeIdVar = $(this).attr('data-placeid');
		
		$.get('/suggestGlasgow/DislikePlace/',
			{'place_id': placeIdVar},
			function(data) {
				$('#dislike_count').html(data);
				$('#dislike_btn').hide();
				$('#like_btn').hide();
				//maybe show the image?
			})
	});
});

$(document).ready(function() {
	$('#save_btn').click(function() {
		var placeIdVar;
		placeIdVar = $(this).attr('data-placeid');
		
		$.get('/suggestGlasgow/SavePlace/',
			{'place_id': placeIdVar},
			function(data) {
				$('#save_count').html(data);
				$('#save_btn').hide();
				//maybe change save_btn to unsave_btn?
			})
	});
});


$(document).ready(function(){
  $(document).on('click', '#like', function(event){
    event.preventDefault();
    var pk = $(this).attr('value');
    $.ajax({
      type: 'POST',
      url: '{% url "likes" %}',
      data: {
            'post_id': pk,
            'csrfmiddlewaretoken': '{{ csrf_token }}'
            },
            success: function(response){
              $('#like-section').html(response['form'])
            },
            error: function(rs, e){
              console.log(rs.responseText);
            },
          });
     });
})