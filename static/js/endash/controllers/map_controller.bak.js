/**
 * Created by Lennin Hernandez on 20/11/2016.
 */

var MapControllers=angular.module('MapControllers',[]);

MapControllers.controller('MapController',
    ['$scope', '$http', 'NgMap', function($scope, $http, NgMap){
        // MAP
        var vm = this;

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

		vm.loadMeasures = function(nodeid){
			var url = "/api/nodes/"+nodeid+"/measures/?begin="+vm.beginDate+"&end="+vm.endDate;
			$http.get(url)
			.then(function(response) {
				vm.measures = response.data;
			});
		};

		vm.loadNode = function(nodeid){
			var url = "/api/nodes/"+nodeid+"/";
			$http.get(url)
			.then(function(response) {
				vm.node = response.data;
		        $scope.node = vm.node;
                vm.node.latitude = parseFloat(vm.node.location[0]);
                vm.node.longitude = parseFloat(vm.node.location[1]);
                vm.showMainMap = false;
                vm.node_list_class = "node-list-detail-minimap";

                // add last measure to node
                $http.get("/api/nodes/"+vm.node.id+"/measures/last/").then(function(response){
                	vm.node.last = response.data;
                	dt = moment(vm.node.last.datetime_str);
                	dta = moment();
                	if(dt-dta>15){
                		vm.node.class="green-node";
                	}else{
                		vm.node.class="red-node";
                	}
                });

                // fix picture path
                if (vm.node.photography==null){
                	vm.node.photography="/static/img/no_pic.png";
                }

                vm.loadMeasures(vm.node.id);
			});
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
                        poss = node.location.split(',');;
                        node.position = poss;
                        node.latitude = parseFloat(poss[0]);
                        node.longitude = parseFloat(poss[1]);


                        // add coordinates to vm.coordinates object
                        vm.coordinates[nodes[i].id] = {
                            latitude:node.latitude,
                            longitude:node.longitude
                        };

                        node.class = "red-node";
                        vm.markers.push(node);
                        vm.nodes[node.id] = node;
                        // add last measure to node
                        $http.get("/api/nodes/"+node.id+"/measures/last/").then(function(response){
                            var node2 = vm.nodes[response.data.node_id];
                        	node2.last = response.data;
                        	dt = moment(node2.last.datetime_str);
                        	dta = moment();
                        	if(dt-dta>15){
                        		node2.class="green-node";
                        	}else{
                        		node2.class="red-node";
                        	}
                        	node2.desc = "Ultima medicion el: " + dt.fromNow();
                        });
                        
                        // fix picture path
                        if (node.photography==null){
                        	node.photography="/static/img/no_pic.png";
                        }
                        
                        node.loadNode = function(){vm.loadNode(node.id)};
                        vm.auxnode = null;
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

        $scope.googleMapsUrl="https://maps.googleapis.com/maps/api/js?libraries=placeses,visualization,drawing,geometry,places&key="+__GOOGLE_API_KEY__;


        vm.showDetail = function(e, node) {
            vm.__node = node;
            vm.map.showInfoWindow('foo-iw', "m"+node.id.toString());
        };

        vm.hideDetail = function() {
            vm.map.hideInfoWindow('foo-iw');
        };

        vm.reset = function(){
            vm.nodeid=null;
            vm.showMainMap=true;
            vm.__map = null;
            vm.node_list_class = "node-list-detail-nominimap";
        };
        
        
        vm.chartopts = {
        		chart: {
        			type: 'lineWithFocusChart',
        			height: 450,
        			widht: 700,
        			margin : {
        				top: 20,
        				right: 20,
        				bottom: 60,
        				left: 40
        			},
        			duration: 50,
        			xAxis: {
        				axisLabel: 'X Axis',
        				tickFormat: function(d){
        					return d3.format(',f')(d);
        				}
        			},
        			x2Axis: {
        				tickFormat: function(d){
        					return d3.format(',f')(d);
        				}
        			},
        			yAxis: {
        				axisLabel: 'Y Axis',
        				tickFormat: function(d){
        					return d3.format(',.2f')(d);
        				},
        				rotateYLabel: false
        			},
        			y2Axis: {
        				tickFormat: function(d){
        					return d3.format(',.2f')(d);
        				}
        			}

        		}
        };

        vm.chartdata = generateData();

        /* Random Data Generator (took from nvd3.org) */
        function generateData() {
        	return stream_layers(3,10+Math.random()*200,.1).map(function(data, i) {
        		return {
        			key: 'Stream' + i,
        			values: data
        		};
        	});
        }

        /* Inspired by Lee Byron's test data generator. */
        function stream_layers(n, m, o) {
        	if (arguments.length < 3) o = 0;
        	function bump(a) {
        		var x = 1 / (.1 + Math.random()),
        		y = 2 * Math.random() - .5,
        		z = 10 / (.1 + Math.random());
        		for (var i = 0; i < m; i++) {
        			var w = (i / m - y) * z;
        			a[i] += x * Math.exp(-w * w);
        		}
        	}
        	return d3.range(n).map(function() {
        		var a = [], i;
        		for (i = 0; i < m; i++) a[i] = o + o * Math.random();
        		for (i = 0; i < 5; i++) bump(a);
        		return a.map(stream_index);
        	});
        }

        /* Another layer generator using gamma distributions. */
        function stream_waves(n, m) {
        	return d3.range(n).map(function(i) {
        		return d3.range(m).map(function(j) {
        			var x = 20 * j / m - i / 3;
        			return 2 * x * Math.exp(-.5 * x);
        		}).map(stream_index);
        	});
        }

        function stream_index(d, i) {
        	return {x: i, y: Math.max(0, d)};
        }


    }]);