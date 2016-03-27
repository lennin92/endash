/**
 * Created by Administrador on 22/03/2016.
 */

var generarGrupos = function (lista, t) {
    var l = [];
    var lt = lista.length;
    var i = 0;
    while (l.length < t) l.push([]);
    while (lista.length > 0) {
        l[i % t].push(lista.pop());
        i += 1;
    }
    return l;
};

var dashboardApp = angular.module('DashboardApp', ['ngMaterial', 'ngAnimate', 'ngRoute']);

dashboardApp.config(['$mdThemingProvider', '$routeProvider', '$interpolateProvider',
    function ($mdThemingProvider, $routeProvider, $interpolateProvider) {
        $mdThemingProvider.theme('default').primaryPalette('red', {
            'hue-1': '900', // use shade 100 for the <code>md-hue-1</code> class
        });
        $interpolateProvider.startSymbol('{[{');
        $interpolateProvider.endSymbol('}]}');
        $routeProvider.
        when('/', {
            templateUrl: '/static/dashboard/views/lista.html',
            controller: 'AppCtrl',
            controllerAs: 'vm'
        }).
        when('/nodos/:idNodo', {
            templateUrl: '/static/dashboard/views/nodo.html',
            controller: 'AppCtrl',
            controllerAs: 'vm'
        }).
        otherwise({
            redirectTo: '/'
        });
    }]);

dashboardApp.controller('AppCtrl', ['$scope', '$http', '$window', function ($scope, $http, $window) {
    var vm = this;
    vm.tipoFiltro = 0;
    vm.cargarNodo = function (nodo) {
        $window.location.href = '/#/nodos/' + nodo.id;
    };
    vm.demanda2Text = function (demanda) {
        var d = new Date(demanda.fecha_fin);
        var m = d.getMonth();
        var s = '';
        switch (m) {
            case 0:
                s = '/Ene/';
                break;
            case 1:
                s = '/Feb/';
                break;
            case 2:
                s = '/Mar/';
                break;
            case 3:
                s = '/Abr/';
                break;
            case 4:
                s = '/May/';
                break;
            case 5:
                s = '/Jun/';
                break;
            case 6:
                s = '/Jul/';
                break;
            case 7:
                s = '/Ago/';
                break;
            case 8:
                s = '/Sep/';
                break;
            case 9:
                s = '/Oct/';
                break;
            case 10:
                s = '/Nov/';
                break;
            case 12:
                s = '/Dic/';
                break;
        }
        var txt = 'Al ' + d.getDate() + s + (d.getYear() - 100) + '';
        return txt;
    };
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
    vm.filtrarNodos = function () {
        var url = '';
        if (vm.tipoFiltro == 0) url = '/rest-api/nodos/?format=json';
        else url = '/rest-api/nodos/padres/?format=json';

        $http.get(url).then(function (response) {
            var res = response.data;
            var arr = [];
            for (var i = 0; i < res.length; i++) {
                if (res[i].fotografia == null) res[i].fotografia = '/static/dashboard/img/none.png';
                arr.push(angular.extend({}, res[i]));
            }
            vm.nodos = arr;
            vm.grupos = generarGrupos(vm.nodos.slice(), 4);
        });
    };
}]);