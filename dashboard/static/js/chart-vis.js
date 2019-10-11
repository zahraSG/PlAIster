$(document).ready(function(){
    //console.log(act)
    if (act=="stop"){
      return;
    }
    if (act=="go"){
      var graphCreate;     //varibla for the graph name
      var DELAY = 6000;    //iteration for each 2.5s
      var MINy = -20;      //initial minimum range for the graph
      var MAXy = 100;      //initial maximum range for the graph
      var contain = document.getElementById(deviceName);  // Create a graph2d with an (currently empty) dataset
      var data= new vis.DataSet();   // Define datasets of the graph2d
      var groups =new vis.DataSet();  // this option holds when more than 1 plot is visualized. grouping is how to do it.
      groups.add({
        id: 0,
          content: deviceName,
      })
      // Define option of the graph (check vis.js documentation fo more info :http://visjs.org/docs/graph2d/ )
      var options = {
          start: vis.moment().add(-4600, 'seconds'), 
          end: vis.moment(),
          width:  '98%',
          height: '210px',
          dataAxis: {
                left: { range: { min:MINy, max: MAXy },},
            },
          drawPoints: {
	      size: 1,
              style: 'circle' 
          },
          shaded: {
              orientation: 'bottom' 
          },
          autoResize : false,
          moveable: true,
          zoomable: true,
          clickToUse: true,
	  interpolation: false,
      };
      // create graphs (for each container dataset, container is the div at html template)
      graphCreate = new vis.Graph2d(contain, data, groups, options);
      renderStep(graphCreate, DELAY);
      addDataPoint(graphCreate,data, DELAY,crownID,name_select,macaddress);

      /**
  * this function renders the step of the graph by moving the window range per tie stamp
  */
      function renderStep(graph, DELAY) {
      // move the window (you can think of different strategies).
      var now = vis.moment();
      var range = graph.getWindow();
      var interval = range.end - range.start;
      // move the window 90% to the left when now is larger than the end of the window
      graph.setWindow(now - interval, now, {animation: true} );
      setTimeout(() => {renderStep(graph, DELAY)}, DELAY);
      }

      /**
   * this function get ste data from python code for reading the data from database and removes the old data  from the screen.
   */
      function addDataPoint(graph,dataset, DELAY, crownID,name_select,macaddress) {
        // cownID is exactly the parameter that is being passed to the python code so should have the exact same name. if more parameters are required all should be passed in a dictenay form
        jQuery.get('/_update',{ crownID: crownID, deviceName:name_select, macaddress:macaddress}, function(data, status) {
          //  In order to not passing a data to vis chart when the data is NAN and it is not availbe :
          if (isNaN(data)) {
            console.log("no data availble");
            return 
            }
            else {
             var now = vis.moment();
             dataset.add({
               x: now,
               y: data,
             });
             if (data > MAXy ){
               MAXy=data +50
             }
             else if (data < MINy ){
               MINy=data
             }
           }
           }, "json"
         );

        // remove all data points which are no longer visible
        var range = graph.getWindow();
        var interval = range.end - range.start;
        var oldIds = dataset.getIds({
          filter: function (item) {
            return item.x < range.start - interval;
          }
        });
        // to scale the format to the maximum and minimum of all time
        graph.setOptions({
        dataAxis: {
            left: { range: {min:MINy, max: MAXy},}}
          })
        dataset.remove(oldIds);
        setTimeout(() => {addDataPoint(graph,dataset, DELAY,crownID,name_select,macaddress)}, DELAY);
      }

    }
});
