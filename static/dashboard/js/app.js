/**
 * Created by Administrador on 22/03/2016.
 */


var dashboardApp = angular.module('DashboardApp', ['ngMaterial']);

dashboardApp.config(function($mdThemingProvider) {
  $mdThemingProvider.theme('default')
    .primaryPalette('red');
});

dashboardApp.controller('AppCtrl', ['$scope', '$http', function($scope, $http) {
    var getImagePath = function() {
    	if(Math.random()<.5) {
    		return '//static/dashboard/img/400x16-9.png';
    	}
    	else {
    		return '//static/dashboard/img/225x9-16.png';
    	}
    };

	var vm = this;
	vm.nodos=[];
	$http.get('/rest-api/nodos/?format=json').then(function(response){
		var res=response.data;
		var arr =[];
		for(var i=0;i<res.length;i++) {
			if(res[i].fotografia==null) res[i].fotografia='//static/dashboard/img/none.png';
			arr.push(angular.extend({}, res[i]));
		}
		vm.nodos = arr;
	});
}]);