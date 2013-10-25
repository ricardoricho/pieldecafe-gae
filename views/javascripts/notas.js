$(document).ready(function(){
	$('.borrar').click(function(){
		var borrar = confirm("Se borrará la nota");
		if(borrar){
			jQuery.ajax({
				type: 'DELETE',
				url : $(this).attr('href'),
				dataType: 'json',
				success:  function(data){
					window.location = '/notas';
				}
			});	
		}		
		return false;
	});
});
