/**
 * Created by Lennin Hernandez on 20/11/2016.
 */

var MapControllers=angular.module('MapControllers',[]);

MapControllers.controller('MapController',
    ['$scope', '$http', 'uiGmapGoogleMapApi', function($scope, $http, uiGmapGoogleMapApi){
        // MAP
        var vm = this;
        vm.markers = [];

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
                        vm.markers.push(node);

                        // add coordinates to vm.coordinates object
                        vm.coordinates[nodes[i].id] = {
                            latitude:node.latitude,
                            longitude:node.longitude
                        };
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
                    console.log(vm.lines);
                });
        };


        vm.map = mapOptions;
        vm.options= {scrollwheel: true};
        uiGmapGoogleMapApi.then(function(maps) {
            loadMarkersAndLines();
        });

    }]);