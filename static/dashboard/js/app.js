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

// DJANGO FORMAT FOR DATE TIME YYYY-MM-DD HH:MM
Date.prototype.dF = function () {
    var yyyy = this.getFullYear().toString();
    var mm = (this.getMonth() + 1).toString(); // getMonth() is zero-based
    var dd = this.getDate().toString();
    var mn = this.getMinutes().toString();
    var hh = this.getHours().toString();
    return yyyy + '-'
        + (mm[1] ? mm : "0" + mm[0]) + '-'
        + (dd[1] ? dd : "0" + dd[0]) + ' '
        + (hh[1] ? hh : "0" + hh[0]) + ':'
        + (mn[1] ? mn : "0" + mn[0]);
};

var dashboardApp = angular.module('DashboardApp', ['ngMaterial', 'ngAnimate',
    'ngRoute', 'angularChart', 'openlayers-directive']);

dashboardApp.config(['$mdThemingProvider', '$routeProvider', '$interpolateProvider',
    function ($mdThemingProvider, $routeProvider, $interpolateProvider) {
        $mdThemingProvider.theme('default').primaryPalette('red', {
            'hue-1': 'A700', // use shade 100 for the <code>md-hue-1</code> class
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
            controller: 'NodoCtrl',
            controllerAs: 'vm'
        }).
        when('/mapa', {
            templateUrl: '/static/dashboard/views/mapa.html',
            controller: 'MapCtrl',
            controllerAs: 'vm'
        }).
        otherwise({
            redirectTo: '/'
        });
    }]);

dashboardApp.controller('MapCtrl', ['$scope', '$http', function ($scope, $http) {
    var vm = this;
    vm.center = {lat: 13.719363, lon: -89.203081, zoom: 16};
    $http.get('/rest-api/nodos/?format=json').then(function (response) {
        var res = response.data;
        var arr = [];
        var marcadores = [];
        for (var i = 0; i < res.length; i++) {
            if (res[i].fotografia == null) res[i].fotografia = '/static/dashboard/img/none.png';
            arr.push(angular.extend({}, res[i]));
            n = res[i];
            if (n.coordenada != null)
                marcadores.push(angular.extend({}, {
                    "name": n.nombre, "lat": n.coordenada.coordinates[0],
                    "lon": n.coordenada.coordinates[1],
                    "label": {
                        "message": n.nombre,
                        "show": false,
                        "showOnMouseOver": true
                    }
                }));
        }
        vm.nodos = arr;
        vm.marcadores = [];
    });
}]);

dashboardApp.controller('NodoCtrl', ['$scope', '$http', '$window', '$routeParams',
    function ($scope, $http, $window, $routeParams) {
        var vm = this;
        vm.xAxisTickFormatFunction = function () {
            return function (d) {
                return d3.time.format('%x')(new Date(d));  //uncomment for date format
            }
        };

        vm.tipoFiltro = 0;
        vm.cargarNodo = function (nodo) {
            $window.location.href = '/#/nodos/' + nodo.id;
        };
        vm.demanda2Text = demanda2Text;
        vm.nodos = [];
        vm.grupos = [];
        vm.idNodo = $routeParams.idNodo;
        vm.aplicarFiltroFechas = function () {
            var url = '/rest-api/mediciones/?format=json&nodo=' + vm.idNodo + '&begin=' + vm.desde.dF() + '&end=' + vm.hasta.dF();
            $http.get(url).then(function (response) {
                vm.mediciones = response.data;
                vm.data = vm.mediciones;
                vm.options = {
                    data: vm.data,
                    dimensions: {
                        demanda: {axis: 'y'},
                        energia_activa: {axis: "y2"},
                        energia_aparente: {axis: "y2"},       // leave the object empty to add a line to the y-Axis
                        fecha_hora: {
                            axis: 'x',
                            displayFormat: '%Y-%m-%d %H:%M:%S',
                            dataType: 'datetime',
                            dataFormat: '%Y-%m-%dT%H:%M:%SZ',
                            name: 'Date'
                        }
                    },
                    chart: {
                        subchart: {
                            show: true
                        }
                    }
                };
            });
        };
        $http.get('/rest-api/nodos/' + vm.idNodo + '/?format=json').then(function (response) {
            var res = response.data;
            if (res.fotografia == null) res.fotografia = '/static/dashboard/img/none.png';
            vm.nodo = res;
            $http.get('/rest-api/nodos/' + vm.idNodo + '/hijos/?format=json').then(function (response) {
                var res = response.data;
                var arr = [];
                for (var i = 0; i < res.length; i++) {
                    if (res[i].fotografia == null) res[i].fotografia = '/static/dashboard/img/none.png';
                    arr.push(angular.extend({}, res[i]));
                }
                vm.nodos = arr;
                vm.grupos = generarGrupos(vm.nodos.slice(), 4);
            });
        });

        var hoy = new Date();
        var inicio = new Date(hoy.getYear() + 1900, hoy.getMonth(), 1);
        vm.desde = inicio;
        vm.hasta = hoy;
        vm.aplicarFiltroFechas();

    }]);


dashboardApp.controller('AppCtrl', ['$scope', '$http', '$window', function ($scope, $http, $window) {
    var vm = this;
    vm.tipoFiltro = 0;
    vm.cargarNodo = function (nodo) {
        $window.location.href = '/#/nodos/' + nodo.id;
    };
    vm.demanda2Text = demanda2Text;
    vm.nodos = [];
    vm.grupos = [];
    $http.get('/rest-api/nodos/?format=json').then(function (response) {
        var res = response.data;
        var arr = [];
        for (var i = 0; i < res.length; i++) {
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

var demanda2Text = function (demanda) {
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

var DemoData = function () {

    var climateData = [
        {temp: -1, rain: 100, sun: 2, month: 'Jan', date: '2014-01-01', num: 13},
        {temp: 2, rain: 80, sun: 3, month: 'Feb', date: '2014-02-01', num: 14},
        {temp: 7, rain: 90, sun: 5, month: 'Mar', date: '2014-03-01', num: 15},
        {temp: 11, rain: 60, sun: 7, month: 'Apr', date: '2014-04-01', num: 16},
        {temp: 15, rain: 50, sun: 9, month: 'May', date: '2014-05-01', num: 17},
        {temp: 22, rain: 15, sun: 12, month: 'Jun', date: '2014-06-01', num: 18},
        {temp: 25, rain: 10, sun: 12, month: 'Jul', date: '2014-07-01', num: 19},
        {temp: 28, rain: 5, sun: 13, month: 'Aug', date: '2014-08-01', num: 20},
        {temp: 27, rain: 30, sun: 2, month: 'Sep', date: '2014-09-01', num: 21},
        {temp: 21, rain: 60, sun: 6, month: 'Oct', date: '2014-10-01', num: 22},
        {temp: 14, rain: 70, sun: 9, month: 'Nov', date: '2014-11-01', num: 23},
        {temp: 5, rain: 80, sun: 5, month: 'Dec', date: '2014-12-01', num: 24}
    ];

    return {
        data: climateData
    };

}