// var goodreadApp = angular.module('goodreadApp', ['nya.bootstrap.select']);
var goodreadApp = angular.module('goodreadApp', []);

// goodreadApp.config(function ($interpolateProvider) {
//     $interpolateProvider.startSymbol('[[');
//     $interpolateProvider.endSymbol(']]');
// });

goodreadApp.controller('goodreadController', function PhoneListController($scope, $http, $timeout) {
    $scope.runmodelLoader = false;
    $scope.topics = null
    $timeout(function() {
        $('.selectpicker').selectpicker('refresh');
    });
    $http.get("/topics")
        .then(function successCallback(response){
            // console.log(response.data);
            $scope.topics = response.data;
            // $('select').selectpicker("destroy");
            // $('select').selectpicker("render"); 
            console.log($scope.topics)
        }, function errorCallback(response){
            console.log("Unable to perform get request");
        });
    
    $scope.tags = [];

    $scope.queryTopics = function() {
        return $scope.topics;
    };

    $scope.getArticles = function(){
        // console.log($scope.selectedTopics)
        var data = $scope.selectedTopics.join();
        console.log(data)

        $http.get("/articles?q="+data)
        .then(function successCallback(response){
            console.log("got articles")
            $scope.articles = response.data.data;
            console.log(response.data.data)
            $scope.runmodelLoader = false;
        }, function errorCallback(response){
            console.log("Unable to perform get request");
            $scope.runmodelLoader = false;
        });

    }
    
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