/**
 * Created by Lennin Hernandez on 20/11/2016.
 */

var MapControllers=angular.module('MapControllers',[]);

MapControllers.controller('MapController',
    ['$scope', '$http', 'uiGmapGoogleMapApi', function($scope, $http, uiGmapGoogleMapApi){
        // MAP
        var vm = this;
        vm.markers = [];
		vm.nodes = {};

        var mapOptions = {
            zoom: 17,
            center:  {latitude: 13.7193289, longitude: -89.2027828}
        };

        vm.window= {
            marker: {},
            show: false,
            closeClick: function() {
                this.show = false;
                this.title = '';
                this.model = null;
            },
            options: {}, // define when map is ready
            title: '',
            model:null
        };

        vm.markerEvents = {
            click : function(marker, event, node){
                vm.window.model = node;
                vm.window.title = node.name;
                vm.window.show = true;
            }
        };

        // PolyLines array (object array containing latitude and longitude)
        vm.lines = [];
        // Coordinates array: object that maps node id with its latitude and longitude.
        vm.coordinates={};

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
                                {latitude: node.latitude, longitude: node.longitude},
                                parent,
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


        vm.map = mapOptions;
        vm.options= {scrollwheel: true};
        
        

		vm.beginDate = moment().subtract(17, 'days');
		vm.endDate = moment();
		vm.measures = [];
		vm.node = null;
		vm.showMainMap = true;
		
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
                vm.node.latitude = parseFloat(vm.node.location[0]);
                vm.node.longitude = parseFloat(vm.node.location[1]);
                vm.showMainMap = false;
                
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
		
		vm.reset = function(){
			vm.measures = [];
			vm.node = null;
			vm.showMainMap = true;			
		};
        
        vm.showMainMap = true;
        
        uiGmapGoogleMapApi.then(function(maps) {
            loadMarkersAndLines();
        });
        
        

    }]);