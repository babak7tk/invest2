app.controller('myCtrl', function ($scope, $http) {
                {% include 'auth/auth.js' %}

                $scope.id = null;
                $scope.data = null;
                $scope.is_submited = '';
                $scope.is_confirm_info_1 = false;

                $scope.errors = [];

                $scope.user_types = [
                    {'id' : 'genuine', 'name' : 'حقیقی'},
                    {'id' : 'legal', 'name' : 'حقوقی'},
                ];

                $scope.init = function () {
                    {% if request.user.is_staff %}
                        $scope.is_confirm_info_1 = true;
                        $scope.GetReqData();
                    {% endif %}
                }

                // Request Data
                $scope.GetReqData = function () {
                    $scope.is_submited = true;

                    var url = `/api/request/{{ object.id }}/`;

                    $http.get(url).then(res => {
                        $scope.is_submited = false;
                        $scope.data = res.data;

                    }).catch(err => {
                        $scope.is_submited = false;
                        parseError(err, 'خطایی رخ داد');
                    });
                }


                $scope.SubmitReqData = function () {
                    fd = new FormData();

                    for(const item in $scope.data){
                        if($scope.data[item]){
                            fd.append(item, $scope.data[item]);
                        }
                    }

                    var files = [
                        'capital_markets_file',
                        'analyst_file',
                        'portfolio_management_file',
                        'securities_valuation_file',
                        'cfa_file',
                        'frm_file',
                        'cia_file',
                        'cma_file',
                        'insurance_report_file',
                    ];

                    for (const item in files) {
                        if ($(`#id_${files[item]}`)[0].files[0]) {
                            fd.append(`${files[item]}`, $(`#id_${files[item]}`)[0].files[0]);
                        }
                        {% comment %} else{
                            fd.append(`${files[item]}`, null);
                        } {% endcomment %}
                    }

                    $scope.is_submited = true;

                    var url = `/api/request/`;

                    $http.post(url, fd, {
                        headers: {
                            'Content-Type': undefined
                        },
                    }).then(res => {
                        createToast('success', 'اطلاعات شما با موفیت ذخیره شد.');
                        console.log(res.data)
                        setTimeout(() => {
                            $scope.is_submited = false;
                            location.reload();
                        }, 3000);
                    }).catch(err => {
                        $scope.is_submited = false;

                        if (err['data']['non_field_errors']) {
                            $scope.errors = err['data']['non_field_errors'];
                            createToast('error', err['data']['non_field_errors'][0]);
                            return;
                        }

                        for (const item in err['data']) {
                            if (err['data']) {
                                $scope.errors = err['data'];
                                return;
                            }
                        }
                        parseError(err, 'خطایی رخ داد');
                    });
                }
            }
        );


app.directive('validFile',function(){
  return {
    require:'ngModel',
    link:function(scope,el,attrs,ngModel){
      //change event is fired when file is selected
      el.bind('change',function(){
        scope.$apply(function(){
          ngModel.$setViewValue(el.val());
          ngModel.$render();
        });
      });
    }
  }
});