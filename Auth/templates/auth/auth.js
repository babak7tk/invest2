$scope.window = window;
$scope.intervalId = 0;
$scope.counter = 0;

// Counter here
function clearTimer() {
    clearInterval($scope.intervalId);
}

function countDown() {
    clearTimer();
    $scope.counter = 60;
    $scope.intervalId = $scope.window.setInterval(() => {
        $scope.counter -= 1;
        // console.log($scope.counter);
        if ($scope.counter === 0) {
            clearTimer();
        }

        // I had to apply below method, because it was not working in the proper way!!!
        $scope.$apply(function () {
            $scope.intervalId = $scope.intervalId;
        });
    }, 1000);
}
