/**
 * Created by Administrador on 22/03/2016.
 */


var dashboarApp = angular.module('DashboardApp', ['ngMaterial']);

dashboarApp.config(function($mdThemingProvider) {
  $mdThemingProvider.theme('default')
    .primaryPalette('red')
    .dark();
});

dashboarApp.controller('AppCtrl', function($scope) {
    var getImagePath = function() {
    	if(Math.random()<.5) {
    		return '//static/dashboard/img/400x16-9.png';
    	}
    	else {
    		return '//static/dashboard/img/225x9-16.png';
    	}
    };

    var photos = [];

    for(var i = 0; i < 25; i++) {
    	photos.push({
    		id: i,
    		path: getImagePath()
    	});
    }

    $scope.fotos = photos;

});