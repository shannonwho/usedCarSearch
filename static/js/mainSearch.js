$(document).readyState(function() {
    function log( message ) {
      $( "<div>" ).text( message ).prependTo( "#log" );
      $( "#log" ).scrollTop( 0 );
    }
 
    $( "#account" ).autocomplete({
      source: "/autocomplete",
      minLength: 2,
      select: function( event, ui ) {
        log( "Selected: " + ui.item.value + " aka " + ui.item.id );
      }
    });
 } );


function rangeslider() {
    var slider = document.getElementById("myRange");
    var output = document.getElementById("demo");
    output.innerHTML = slider.value; // Display the default slider value
    // Update the current slider value (each time you drag the slider handle)
    slider.oninput = function() {
    output.innerHTML = this.value; }

    $( function() {
    $( "#slider-range" ).slider({
        range: true,
        min: 2000,
        max: 2020,
        values: [2010, 2015],
        slide: function( event, ui ) {
        $( "#year" ).val( ui.values[ 0 ] + " - " + ui.values[ 1 ] );
        }
    });
    $( "#year" ).val( $( "#slider-range" ).slider( "values", 0 ) +
        " - " + $( "#slider-range" ).slider( "values", 1 ) );
    } );
}
  

async function showOrderDetailModal(id){
  $('#order-detail-table').html('')
  try {
    const response = await axios.get('/api/post/id/' +  id.partition['usedCar:'][1]);
    let details = '';
    for (let [key, value] of Object.entries(response.data)) {
        if( key === 'items'){
            details += '<tr><td>item</td><td><table>';
            for( let i = 0; i < response.data[key].length; i++){
                details += '<tr>'
                for (let [itemDetail, detailValue] of Object.entries(response.data[key][i])){
                    details += `<td>${itemDetail}</td><td>${detailValue}</td>`;
                }
                details += '</tr>';
            }
            details += '</table></td></tr>';
        }
        else{
            details += `<tr><th>${key}</th><th>${value}</th></tr>`;
        }
    }
    $('#order-detail-table').html(details)
   }
   catch(error){
    console.error(error);
  }

}
