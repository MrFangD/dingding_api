const app = getApp();
Page({
  onLoad(query) {
    // 页面加载
    console.info(`Page onLoad with query: ${JSON.stringify(query)}`);

  },
  onReady() {
    // 页面加载完成
  },
  onShow() {
    // 页面显示
    dd.showLoading({
      content: '加载中...',
    });
    var that = this;
    console.log('xingm',  app.globalData.zgxm)
    dd.httpRequest({
       headers: {
        "Content-Type": "application/json"
      },
      url: 'http://124.133.235.142:9020/getxsddlist',
      method: 'POST',
      data:JSON.stringify({
        "zdr": app.globalData.zgxm
        // "zdr": "123"
      }),
      dataType: 'json',
      success: function(res) {
        var list = [res.data];
        // list = [{'1':1}]
        console.log('加载', list[0].length)
        if (list[0].length == 0) {
          that.setData({
            listData:{
              ontap: 'ListItemTap',
              data: []
              },
            order_sl:0
          })
          dd.hideLoading();
          // dd.alert({
          //   content: '数据为空!!',
          //   buttonText: '确定'
          // });
          return;
        }
        that.setData({
          listData:{
            ontap: 'ListItemTap',
            data: list[0]
            }
        })
        getApp().globalData.xsddbt = list[0]
        dd.hideLoading();
      },
      fail: function(res) {
        console.log(res);
        dd.hideLoading();
      },
      complete: function(res) {
        // console.log(res);
      }
    });
  },
  ListItemTap(e){
    var index = e.currentTarget.dataset.index;
    console.log('备注',this.data.listData.data[index].bz)
    getApp().globalData.lswlzd = this.data.listData.data[index].xsddmx;
    var wldw = {'dwbh':this.data.listData.data[index].khbh ,'dwmc':this.data.listData.data[index].khmc}
    getApp().globalData.zwwldw = wldw
    getApp().globalData.xgindex = index;

    dd.navigateTo({            
      // 保留当前页面，跳转到应用内的某个指定页面
      url: "../delxsdd/index?djzt="+this.data.listData.data[index].djzt+"&bz="+this.data.listData.data[index].bz
    })
  },
  onHide() {
    // 页面隐藏
  },
  onUnload() {
    // 页面被关闭
  },
  onTitleClick() {
    // 标题被点击
  },
  onPullDownRefresh() {
    // 页面被下拉
  },
  onReachBottom() {
    // 页面被拉到底部
  },
  onShareAppMessage() {
    // 返回自定义分享信息
    return {
      title: 'My App',
      desc: 'My App description',
      path: 'pages/index/index',
    };
  },
  data: {
    listData: {
      onItemTap: 'handleListItemTap',
      header: '',
      data: []
    },
    order_sl:1
  }
});
