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
    		return 'http://dummyimage.com/400x16:9';
    	}
    	else {
    		return 'http://dummyimage.com/225x9:16';
    	}
    }

    var partition = function (input, size) {
        var newArr = [];
        for (var i = 0; i < input.length; i += size) {
            newArr.push(input.slice(i, i + size));
        }
        return newArr;
    }

    var photos = [];

    for(var i = 0; i < 100; i++) {
    	photos.push({
    		id: i,
    		path: getImagePath()
    	})
    }

    $scope.data = {
        photos: photos,
        photos3p: partition(photos, photos.length / 4)
    };

});