// Onclick of the button
function generate_linesheet(){
  Notiflix.Loading.standard('Generating ...');
  brand = document.getElementById("brand").value
  template = document.getElementById("template").value
  sku = document.getElementById("sku").value
  launch_date = document.getElementById("launch_date").value
  stock_source = document.getElementById("stock_source").value
  sale_channel = document.getElementById("sale_channel").value
  production_type = document.getElementById("production_type").value
  // Call python's random_python function
  eel.generate_form(brand,template,sku,launch_date,stock_source,sale_channel,production_type)(function(data){
    Notiflix.Loading.change('Finnish .. Excel file are opening ..');
    // Update the div with a random number returned by python
    document.getElementById("generate_status").innerHTML = data;
    Notiflix.Loading.remove();
  })

}

//
function open_linesheet(file){

  eel.open_linesheet(file)(function(data){
      document.getElementById("generate_status").innerHTML = data;

  })
}









