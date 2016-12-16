/**
 * Created by Lennin Hernandez on 20/11/2016.
 */

var MapControllers=angular.module('MapControllers',[]);

MapControllers.controller('MapController',
    ['$scope', '$http', 'NgMap', '$mdSidenav', function($scope, $http, NgMap, $mdSidenav){
        // MAP
        var vm = this;
        $scope.toggleSidebar = function(){
            $mdSidenav('sidebar').toggle();
        };
        $scope.fecha_fin = moment().toDate();
        $scope.fecha_inicio = moment().subtract(7,'day').toDate();
        
        NgMap.getMap("ngmap1").then(function(map) {
            console.log('map', map);
            vm.map = map;
        });

        vm.markers = [];
        vm.nodes = {};
        vm.nodeid=null;
        vm.showMainMap=true;
        vm.__map = null;
        vm.node_list_class = "node-list-detail-nominimap";
        // PolyLines array (object array containing latitude and longitude)
        vm.lines = [];
        // Coordinates array: object that maps node id with its latitude and longitude.
        vm.coordinates={};
        vm.map = {zoom: 17, center:'13.7193289, -89.2027828'};
        vm.pliego = null;
        vm.lecturas = null;
        vm.loadMeasures = function(nodeid){
            var begin = moment($scope.fecha_inicio).format('YYYY-MM-DD HH:mm');
            var end = moment($scope.fecha_fin).format('YYYY-MM-DD HH:mm');
            var url = "/api/nodes/"+nodeid+"/measures/?begin="+begin+"&end="+end;
            $http.get(url)
                .then(function(response) {
                    vm.measures = response.data;
                    $scope.labels = [];
                    $scope.data = [];
                    var activas = [];
                    var aparentes = [];
                    var demandas = [];
                    for(var i=0; i<vm.measures.length; i++){
                        var m = vm.measures[i];
                        $scope.labels.push(m.datetime_str);
                        demandas.push(m.demand);
                        aparentes.push(m.apparent);
                        activas.push(m.active);
                    }
                    $scope.data = [
                        demandas,
                        activas,
                        aparentes
                    ];
                    
                    $http.get('/api/tariff_schedule/'+vm.node.supplier.id+'/').then(function(response){
                    	vm.pliego = response.data[0];
                    	vm.lecturas = [];
                    	vm.facturacion = [];
                    	var format = 'hh:mm:ss';
                    	for(var j=0;j<vm.pliego.tariff_values.length;j++){
                    		var variable = vm.pliego.tariff_values[j];
                    		var lecs = {name:"Consumo en " + variable.name} , sum=0.0;
                    		var cargo = {name: 'Cargo por ' + variable.name}, v_cargo=1;
                    		if(variable.over_max_demand){
                    			var max=0;
	                    		for(var u=0; u<vm.measures.length; u++){
	                    			var measure = vm.measures[u];
	                    			if(max<measure.demand) max=measure.demand;
	                    		}
	                    		sum=max;
	                    		v_cargo=sum*variable.charge_value / 1000.0;
                    		} else if(variable.is_fixed){
                    			sum=variable.charge_value;
	                    		v_cargo=sum;
                    		} else {
                        		var var_begin = moment(variable.consume_begins, format);
                        		var var_ends = moment(variable.consume_ends, format);
	                    		for(var x=0; x<vm.measures.length; x++){
	                    			var measure = vm.measures[x];
	                    			var mea_time = moment(measure.datetime_str.substring(11), format);
	                    			if(var_ends.isBefore(var_begin)){
	                    				if(mea_time.isBetween(var_begin, moment("23:59:59",format)) || mea_time.isBetween(moment("00:00:00",format), var_ends)){
		                    				sum = sum + measure.active;
		                    			}
	                    			} else if(mea_time.isBetween(var_begin, var_ends)){
	                    				sum = sum + measure.active;
	                    			}
	                    		}
	                    		v_cargo = variable.charge_value * sum / 1000.0;
                    		}
                			lecs.consumo = sum;
                			cargo.cargo = v_cargo;
                        	vm.lecturas.push(lecs);
                        	vm.facturacion.push(cargo);
                    	}
                    	var subtotal=0.0, iva=0.0, total=0.0;
                    	for(var k=0;k<vm.facturacion.length;k++){
                    		subtotal = subtotal + vm.facturacion[k].cargo;
                    	}
                    	iva = 0.13 * subtotal;
                    	total = iva + subtotal;
                    	vm.facturacion.push({name:'Subtotal', cargo: subtotal});
                    	vm.facturacion.push({name:'IVA', cargo: iva});
                    	vm.facturacion.push({name:'Total', cargo: total});
                    });
                });
        };

        vm.reset = function(){
            vm.measures = [];
            vm.node = null;
            $scope.node = vm.node;
            vm.showMainMap = true;
            vm.node_list_class = "node-list-detail-nominimap";
            vm.nodeid=null;
            $scope.labels = [];
            $scope.series = ['Demanda', 'Activa', 'Aparente'];
            $scope.data = [];
        };

        vm.loadNode = function(nodeid){
            var url = "/api/nodes/"+nodeid+"/";
            vm.node = vm.nodes[nodeid];
            $scope.node = vm.node;
            /*
             vm.node.position = vm.node.location;
             vm.node.latitude = parseFloat(vm.node.location[0]);
             vm.node.longitude = parseFloat(vm.node.location[1]);
             */
            // vm.node_list_class = "node-list-detail-minimap";
            vm.showMainMap = false;

            // add last measure to node
            $http.get("/api/nodes/"+vm.node.id+"/measures/last/").then(function(response){
                vm.node.last = response.data;
            });

            // fix picture path
            if (vm.node.photography==null){
                vm.node.photography="/static/img/no_pic.png";
            }

            vm.loadMeasures(vm.node.id);
        };
        

        $scope.createLoadNode = function(nodeid){
        	return function(){vm.loadNode(nodeid)};
        };

        var loadMarkersAndLines = function(){
            vm.markers = [];
            $http.get("/api/nodes/")
                .then(function(response) {
                    var node=null;
                    var nodes = response.data;
                    var poss;
                    // Put nodes on vm.markers array
                    for(var i=0;i<nodes.length; i++){
                        node = nodes[i];
                        poss = node.location.split(',');
                        node.position = poss;
                        node.latitude = parseFloat(poss[0]);
                        node.longitude = parseFloat(poss[1]);


                        // add coordinates to vm.coordinates object
                        vm.coordinates[nodes[i].id] = {
                            latitude:node.latitude,
                            longitude:node.longitude
                        };

                        // add last measure to node
                        $http.get("/api/nodes/"+node.id+"/measures/last/").then(function(response){
                            var node2 = vm.nodes[response.data.node_id];
                            node2.last = response.data;
                            dt = moment(node2.last.datetime_str, "YYYY-MM-DD HH:mm");
                            dta = moment(node2.last.datetime_str, "YYYY-MM-DD HH:mm").subtract(7,'day');
                            node2.desc = "Ultima medicion " + dt.fromNow();
                            $scope.fecha_fin = dt.toDate();
                            $scope.fecha_inicio = dta.toDate();
                        });

                        // fix picture path
                        if (node.photography==null){
                            node.photography="/static/img/no_pic.png";
                        }

                        node.loadNode = $scope.createLoadNode(node.id); //function(){vm.loadNode(node.id)};
                        vm.auxnode = null;
                        vm.markers.push(node);
                        vm.nodes[node.id] = node;
                    }
                    // create lines objects
                    for(var i=0;i<nodes.length; i++){
                        node = nodes[i];
                        if (node.parent==null) continue;
                        var parent = vm.coordinates[node.parent];
                        vm.lines.push({
                            id: node.id,
                            path: [
                                [node.latitude, node.longitude],
                                [parent.latitude, parent.longitude],
                            ],
                            stroke:{
                                color: "#19bf00",
                                weight: 2
                            },
                            visible:true,
                            editable:false,
                            draggable:false,
                            geodesic:false
                        });
                    }
                });
        };

        loadMarkersAndLines();


        vm.showDetail = function(e, node) {
            vm.__node = node;
            vm.map.showInfoWindow('foo-iw', 'm' + node.id.toString());
        };

        vm.hideDetail = function() {
            vm.map.hideInfoWindow('foo-iw');
        };

        $scope.labels = [];
        $scope.series = ['Demanda', 'Activa', 'Aparente'];
        $scope.data = [];
        $scope.onClick = function (points, evt) { };
        $scope.datasetOverride = [{ yAxisID: 'y-axis-1' }, { yAxisID: 'y-axis-2' }, { yAxisID: 'y-axis-3' }];
        $scope.options = {
            scales: {
                yAxes: [
                    {
                        id: 'y-axis-1',
                        type: 'linear',
                        display: true,
                        position: 'left'
                    },
                    {
                        id: 'y-axis-2',
                        type: 'linear',
                        display: true,
                        position: 'right'
                    },
                    {
                        id: 'y-axis-3',
                        type: 'linear',
                        display: true,
                        position: 'right'
                    }
                ]
            }
        };
        $scope.colors = [
          '#803690',
          '#00ADF9',
          '#FDB45C',
          '#bf0006',
          '#949FB1'
      ]


    }]);