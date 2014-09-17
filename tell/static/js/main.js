angular.module('tell', ['ngResource'])
      .service('Logger', function($resource) {
        return $resource('/tell/api/loggers/:id');
    }).factory('Entry', function($resource) {
        return $resource('/tell/api/entries/:id');
    }).controller('LoggerController', function($scope, Logger, Entry) {
        var originalNewLogger = {
            'name': "new_logger.log",
            'ip_address': "127.0.0.1:8002",
            'regex': "(\\[(error|warning|info|debug)])"
        };

        $scope.new_logger = angular.copy(originalNewLogger);
        $scope.loggers = Logger.query();

        $scope.addLogger = function() {
            Logger.save(this.new_logger, function() {
                Logger.query(function(result) {
                    $scope.loggers = result;
                });
                $scope.new_logger = angular.copy(originalNewLogger);
            });
        };

        $scope.removeLogger = function(logger) {
            Logger.delete({'id': logger.id}, function() {
                Logger.query(function(result) {
                    $scope.loggers = result;
                });
            });
        }
    }).config(function($interpolateProvider) {
        $interpolateProvider.startSymbol('[[');
        $interpolateProvider.endSymbol(']]');
    }).config(['$resourceProvider', function ($resourceProvider) {
        // Don't strip trailing slashes from calculated URLs
        $resourceProvider.defaults.stripTrailingSlashes = false;
}]);