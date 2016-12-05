/**
 * Created by Lennin Hernandez on 20/11/2016.
 */

var MapControllers=angular.module('NodeControllers',[]);

MapControllers.controller('NodeController',
	['$scope', '$http', '$routeParams', function($scope, $http, $routeParams){
		var vm = this;
		vm.idController = $routeParams.nodeId;
		vm.beginDate = moment().subtract(17, 'days');
		vm.endDate = moment();
		vm.measures = [];
		vm.node = null;
		vm.showMainMap = false;
		
		vm.loadMeasures = function(nodeid){
			var url = "/api/nodes/"+nodeid+"/begin="+vm.beginDate+"&end="+vm.endDate; 
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
                node.latitude = parseFloat(vm.node.location[0]);
                node.longitude = parseFloat(vm.node.location[1]);
                vm.showMainMap = true;
			});		
		};
		
		vm.reset = function(){
			vm.measures = [];
			vm.node = null;
			vm.showMainMap = false;			
		};
		
	}]);