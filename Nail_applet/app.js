App({
  onLaunch(options) {
    //获取用户信息
    // var that = this;
    // dd.getAuthCode({
    //   success:function(res){
    //     dd.httpRequest({
    //       headers: {
    //         "Content-Type": "application/json"
    //       },
    //       url: 'http://127.0.0.1:5000/getuser',
    //       method: 'POST',
    //       data:JSON.stringify({
    //         "code":res.authCode
    //       }),
    //       dataType: 'json',
    //       success: function(res) {
    //         var list = [res.data];
    //         console.log(list[0].name)
    //         that.globalData.zgxm = list[0].name;
    //       },
    //       fail: function(res) {
    //         console.log(res);
    //       },
    //       complete: function(res) {
    //         // console.log(res);
    //       }
    //     });
    //   },
    //   fail:function(err){
    //   }
    // });
  },
  onShow() {
    // my.hideTabBar();
    console.log('App Show');
  },
  onHide() {
    console.log('App Hide');
  },
  globalData: {
    hasLogin: false,
    zwwldw:[],
    lswlzd:[],
    zgxm:"",
    xsddbt:[],
    xsddmx:[],
    xgindex:0
  },
});
