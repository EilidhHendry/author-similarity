var apiRoot = "/";
var classifyUrl = apiRoot + "classify";

var app = angular.module("author", ['ngMaterial']);

app.controller('MainController', function($scope, $document, $timeout, $http, $log) {

    var textarea = document.querySelector('#text');
    // TODO: handle file uploads
    //var fileUpload = document.querySelector('#file');

    $scope.dataModel = {
        text: "test",
        classification: undefined,
    };

    $scope.classify = function() {
        var data = {
            text: $scope.dataModel.text
        };
        $http.post(classifyUrl, data)
        .then(function(successData) {
            var classificationData;
            if ("data" in successData) {
                classificationData = {};
                if ("authors" in successData["data"]) {
                    classificationData["authors"] = successData["data"]["authors"];
                }
                if ("fingerprint" in successData["data"]) {
                    classificationData["fingerprint"] = successData["data"]["fingerprint"];
                }
                $scope.dataModel.classification = classificationData;
                $log.log($scope.dataModel.classification);
            }
        }, function(errorData) {
            $log.log(errorData);
        });
    }

    // TODO: this more sensibly
    $timeout(function() {
        angular.element(textarea.focus());
    })
});
