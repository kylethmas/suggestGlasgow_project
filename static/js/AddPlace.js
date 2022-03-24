function loadMap(){
	var map = new GMap2(document.getElementById("map"));
	map.addControl(new GLargeMapControl());
	map.addControl(new GMapTypeControl());
	
	//set map center (vienna)
	map.setCenter(new GLatLng(48.1985912972919, 16.367568969726562), 12); 
	GEvent.addListener(map, "click", function(overlay, point){
	map.clearOverlays();

	if (point) {
		map.addOverlay(new GMarker(point));
		map.panTo(point);
		msg = "Latitude: "+point.lat()+"<br />"+"Longitude: "+point.lng();
		document.getElementById("mypoint").innerHTML = msg;
		document.getElementById("latitude").value = point.lat(); //models field name 
		document.getElementById("longitude").value = point.lng(); //models field name
	}
}
// arrange for our onload handler to 'listen' for onload events
if (window.attachEvent) {
window.attachEvent("onload", function() {
loadMap();  // Internet Explorer
});
} else {
window.addEventListener("load", function() {
loadMap(); // Firefox and standard browsers
}, false);
}