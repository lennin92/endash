/**
 * Created by Administrador on 22/03/2016.
 */


var dashboardApp = angular.module('DashboardApp', ['ngMaterial', 'ngAnimate', 'ngRoute']);

dashboardApp.config(['$mdThemingProvider', '$routeProvider',
    function ($mdThemingProvider, $routeProvider) {
        $mdThemingProvider.theme('default').primaryPalette('red');
        $routeProvider.
        when('/', {
            templateUrl: '/static/dashboard/views/lista.html',
            controller: 'AppCtrl'
        }).
        when('/nodos/:idNodo', {
            templateUrl: '/static/dashboard/views/nodo.html',
            controller: 'AppCtrl'
        }).
        otherwise({
            redirectTo: '/'
        });
    }]);

dashboardApp.controller('AppCtrl', ['$scope', '$http', function ($scope, $http) {
    var vm = this;
    vm.nodos = [];
    $http.get('/rest-api/nodos/?format=json').then(function (response) {
        var res = response.data;
        var arr = [];
        for (var i = 0; i < res.length; i++) {
            if (res[i].padre == null) res[i].padre = -1;
            if (res[i].fotografia == null) res[i].fotografia = '/static/dashboard/img/none.png';
            arr.push(angular.extend({}, res[i]));
        }
        vm.nodos = arr;
    });
}]);