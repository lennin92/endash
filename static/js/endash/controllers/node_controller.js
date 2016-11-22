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
    }]);