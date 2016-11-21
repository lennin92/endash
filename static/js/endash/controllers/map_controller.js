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



        var loadMarkers = function(){
            vm.markers = [];
            $http.get("/api/nodes/")
                .then(function(response) {
                    var node=null;
                    var nodes = response.data;
                    var poss;
                    for(var i=0;i<nodes.length; i++){
                        node = nodes[i];
                        poss = node.location.split(',');
                        node.latitude = parseFloat(poss[0]);
                        node.longitude = parseFloat(poss[1]);
                        vm.markers.push(node);
                    }
                });
        };


        vm.map = mapOptions;
        vm.options= {scrollwheel: true};
        uiGmapGoogleMapApi.then(function(maps) {
            console.log('olakease');
            loadMarkers();
        });

    }]);