angular.module('tell', ['ngResource'])
      .service('Logger', function($resource) {
        return $resource('/tell/api/loggers/:id');
    }).factory('Entry', function($resource) {
        return $resource('/tell/api/entries/:id');
    }).controller('InvoiceController', function($scope, Logger, Entry) {
        $scope.Logger = Logger;
        $scope.Entry = Entry;
        this.qty = 1;
        this.cost = 2;
        this.inCurr = 'EUR';
        this.currencies = ['USD', 'EUR', 'CNY'];
        this.usdToForeignRates = {
            USD: 1,
            EUR: 0.74,
            CNY: 6.09
        };

        this.total = function total(outCurr) {
            return this.convertCurrency(this.qty * this.cost, this.inCurr, outCurr);
        };
        this.convertCurrency = function convertCurrency(amount, inCurr, outCurr) {
            return amount * this.usdToForeignRates[outCurr] / this.usdToForeignRates[inCurr];
        };
        this.pay = function pay() {
            window.alert("Thanks!");
        };
    }).config(function($interpolateProvider) {
        $interpolateProvider.startSymbol('[[');
        $interpolateProvider.endSymbol(']]');
    }).config(['$resourceProvider', function ($resourceProvider) {
        // Don't strip trailing slashes from calculated URLs
        $resourceProvider.defaults.stripTrailingSlashes = false;
}]);