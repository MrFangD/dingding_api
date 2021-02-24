const app = getApp();
const banks = ['正常销售', '现款销售','免费'];
Page({
  data: {
    buttons: [
      { text: '删除' },
      { text: '修改', extClass: 'buttonBold' },
    ],
    dateValue:'',
    zwdw:'',
    dwbh:'',
    zgbh:"",
    zgxm:"",
    wlsl:0,
    lswlmc:"",
    minsl:"",
    xgindex:0,
    modalOpened: false,
    listData: {
      onLongTap: 'ListItemTap',
      header: '',
      data: []
    },
    bank: '正常销售',
    bz:''
  },
  onLoad(query) {
    // 页面加载
    //获取用户信息
    var that = this;
    that.setData({
      zgxm:app.globalData.zgxm
    })
    dd.showLoading({
      content: '获取用户中...',
    });
    dd.getAuthCode({
      success:function(res){
        console.log(res)
        dd.httpRequest({
          headers: {
            "Content-Type": "application/json"
          },
          url: 'http://124.133.235.142:9020/getuser',
          method: 'POST',
          data:JSON.stringify({
            "code":res.authCode
          }),
          dataType: 'json',
          success: function(res) {
            var list = [res.data];
            that.setData({
              zgxm:list[0].name
            })
            getApp().globalData.zgxm = list[0].name
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
      fail:function(err){
      }
    });
  },
  onReady() {
    // 页面加载完成
    //获取当前日期
    var mydate = new Date();
    console.log('日期',mydate.toLocaleDateString())
    this.setData({
      dateValue:mydate.toLocaleDateString()
    })
  },
  onShow() {
    // 页面显示
    var zwwldw = app.globalData.zwwldw;
    var lswlzd = app.globalData.lswlzd;
    if (zwwldw.length != 0) {
      this.setData({
        zwdw:zwwldw.dwmc,
        dwbh:zwwldw.dwbh
      })
    }
    this.setData({
       listData:{
          onLongTap: 'ListItemTap',
          header: '',
          data: lswlzd
          }
    })
  },
  onSubmit(e) {
    dd.showLoading({
      content: '保存中...',
    });
    if (this.data.zwdw == '') {
      dd.hideLoading();
      dd.alert({
        content: '销售客户允许为空!',
        buttonText: '确定'
      });
      return;
    }
    console.log(this.data.listData.data.length)
    if (this.data.listData.data.length <=0 ) {
      dd.hideLoading();
      dd.alert({
        content: '物料信息不允许为空!',
        buttonText: '确定'
      });
      return;
    }
    dd.httpRequest({
       headers: {
        "Content-Type": "application/json"
      },
      url: 'http://124.133.235.142:9020/xsdd',
      method: 'POST',
      data:JSON.stringify({
        "khbh": this.data.dwbh,
        "khmc": this.data.zwdw,
        "zgxm":this.data.zgxm,
        "ywrq": this.data.dateValue,
        "btxx": this.data.listData.data,
        'ywlx': this.data.bank,
        'bz': this.data.bz
      }),
      dataType: 'json',
      success: function(res) {
        var list = [res.data];
        dd.hideLoading();
        dd.alert({
          content: list[0].info,
          buttonText: '确定',
          success: () => {

          },
        });
      },
      fail: function(res) {
        console.log(res);
        dd.hideLoading();
      },
      complete: function(res) {
        // console.log(res);
      }
    });
    //清空全局变量
    getApp().globalData.zwwldw = [];
    getApp().globalData.lswlzd = [];
    this.setData({
      zwdw:'',
      listData:'',
      bz:''
    })


  },
  onReset(e){
    this.setData({
      zwdw:'',
      listData:'',
      bz:''
    })
    //清空全局变量
    getApp().globalData.zwwldw = [];
    getApp().globalData.lswlzd = [];

  },
  ListItemTap(e){
    var index = e.currentTarget.dataset.index;
    console.log(this.data.listData.data[index])
    this.setData({
      modalOpened: true,
      lswlmc:this.data.listData.data[index].wlmc,
      minsl:this.data.listData.data[index].sl,
      xgindex:index
    });
  },
  onChangeSl(value){
    this.setData({
      wlsl: value,
    });
  },
  onMaskClick(){
    // 关闭涂层
    this.setData({
      modalOpened: false,
    });
  },
  onModalClick(){
    // 数量确认
    if (this.data.wlsl <=0 ) {
      dd.alert({
        content: '数量为0,不允许制单',
        buttonText: '确定'
      });
      return;}
    },
  onButtonClick(e){
    const { target: { dataset } } = e;
    var delindex = this.data.xgindex;
    if (dataset.index == 0) {
      //删除操作
      app.globalData.lswlzd.splice(delindex,1);
      this.setData({
        modalOpened: false
      });
      this.onShow();
    } else {
      //修改操作
      if (this.data.wlsl <=0 ) {
        dd.alert({
          content: '数量为0,不允许制单',
          buttonText: '确定'
        });
        return;
      };
      app.globalData.lswlzd[delindex].sl = this.data.wlsl;
      this.setData({
        modalOpened: false
      });
      this.onShow();
    }
  },
  onFocus(){
    dd.navigateTo({            
      // 保留当前页面，跳转到应用内的某个指定页面
      url: "../zwdw/zwdw?jd=kh"
    })
  },
  onFocus_wl(){
    dd.navigateTo({            
      // 保留当前页面，跳转到应用内的某个指定页面
      url: '../zwdw/zwdw?jd=wl'
    })
  },
  onExtraTap(){
    console.log('$$$$')
    dd.scan({
      type: 'qr',
      success: (res) => {
        dd.alert({ title: res.code });
      },
    });
  },
  onPickerTap() {
    my.showActionSheet({
      title: '选择单据类别',
      items: banks,
      success: (res) => {
        this.setData({
          bank: banks[res.index],
        });
      },
    });
  },
  bindKeyInput(e) {
    console.log( e.detail.value)
    this.setData({
      bz: e.detail.value,
    });
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
      title: '销售下单',
      desc: 'My App description',
      path: 'pages/index/index',
    };
  },
});
