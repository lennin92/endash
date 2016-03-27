/**
 * Created by Administrador on 22/03/2016.
 */

var generarGrupos = function (lista, t){
    var l = [];
    var lt = lista.length;
    var i = 0;
    while(l.length<t) l.push([]);
    while(lista.length>0){
        l[i%t].push(lista.pop());
        i+=1;
    }
    return l;
};

var dashboardApp = angular.module('DashboardApp', ['ngMaterial', 'ngAnimate', 'ngRoute']);

dashboardApp.config(['$mdThemingProvider', '$routeProvider', '$interpolateProvider',
    function ($mdThemingProvider, $routeProvider, $interpolateProvider) {
        $mdThemingProvider.theme('default').primaryPalette('red');
        $interpolateProvider.startSymbol('{[{');
        $interpolateProvider.endSymbol('}]}');
        $routeProvider.
        when('/', {
            templateUrl: '/static/dashboard/views/lista.html',
            controller: 'AppCtrl',
            controllerAs:'vm'
        }).
        when('/nodos/:idNodo', {
            templateUrl: '/static/dashboard/views/nodo.html',
            controller: 'AppCtrl',
            controllerAs:'vm'
        }).
        otherwise({
            redirectTo: '/'
        });
    }]);

dashboardApp.controller('AppCtrl', ['$scope', '$http', function ($scope, $http) {
    var vm = this;
    vm.nodos = [];
    vm.grupos = [];
    $http.get('/rest-api/nodos/?format=json').then(function (response) {
        var res = response.data;
        var arr = [];
        for (var i = 0; i < res.length; i++) {
            if (res[i].padre == null) res[i].padre = -1;
            if (res[i].fotografia == null) res[i].fotografia = '/static/dashboard/img/none.png';
            arr.push(angular.extend({}, res[i]));
        }
        vm.nodos = arr;
        vm.grupos = generarGrupos(vm.nodos.slice(), 4);
    });
}]);