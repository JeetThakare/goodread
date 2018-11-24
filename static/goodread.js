var goodreadApp = angular.module('goodreadApp', []);

goodreadApp.config(function ($interpolateProvider) {
    $interpolateProvider.startSymbol('[[');
    $interpolateProvider.endSymbol(']]');
});

goodreadApp.controller('goodreadController', function PhoneListController($scope, $http) {
    $scope.runmodelLoader = false;

    $scope.runmodel = function (){
        $scope.runmodelLoader = true;
        $http.get("/runmodel")
        .then(function successCallback(response){
            console.log("model ran")
            $scope.runmodelLoader = false;
        }, function errorCallback(response){
            console.log("Unable to perform get request");
            $scope.runmodelLoader = false;
        });
    }      
});