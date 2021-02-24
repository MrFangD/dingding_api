Page({
  onLoad(query) {
    // 页面加载
    this.setData({
      jd:JSON.stringify(query.jd)
    })
  },
  onReady() {
    // 页面加载完成
  },
  onShow() {
    var that = this;
    var url = '';
    var data;

    // 页面显示
    if (that.data.jd == '"kh"') {

      // url='http://124.133.235.142:9020/zwwldw';
      // data = JSON.stringify({
      //   "dwmc": this.data.inputValue
      // })
      that.setData({
        page:1
      })
    } else {
      that.setData({
        page:2
      })
      dd.showLoading({
        content: '检索中...',
      });
      url='http://124.133.235.142:9020/getwllb';
      data = []
      dd.httpRequest({
        headers: {
          "Content-Type": "application/json"
        },
        url: url,
        method: 'POST',
        data:data,
        dataType: 'json',
        success: function(res) {
          var list = [res.data];
          if (list[0].length <=0 ) {
            dd.hideLoading();
            dd.alert({
              content: '未查询到相关数据,请重新查询!',
              buttonText: '确定'
            });
            return;
          }
          // dd.setStorage({
          //   key:'list',
          //   data:list
          // })
          that.setData({
            listData:{
              onItemTap:'onItemTap',
              data:list[0]
            }
          })
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
    }
  },
  onHide() {
    // 页面隐藏
  },
  onUnload() {
    // 页面被关闭
  },
  onShareAppMessage() {
    // 返回自定义分享信息
    return {
      title: 'My App',
      desc: 'My App description',
      path: 'pages/index/index',
    };
  },
  bindKeyInput(e) {
      this.setData({
        inputValue: e.detail.value,
      });
  },
  onSearch(e){
    var that = this;
    var url = '';
    var data;
    dd.showLoading({
      content: '检索中...',
    });
    if (that.data.jd == '"kh"') {
      url='http://124.133.235.142:9020/zwwldw';
      data = JSON.stringify({
        "dwmc": this.data.inputValue
      })
    } else {
      url='http://124.133.235.142:9020/lswlzd';
      data = JSON.stringify({
        "wlmc": this.data.inputValue,
        "wlbh":'',
        "wllb":''
      })
    }
    dd.httpRequest({
       headers: {
        "Content-Type": "application/json"
      },
      url: url,
      method: 'POST',
      data:data,
      dataType: 'json',
      success: function(res) {
        var list = [res.data];
        if (list[0].length <=0 ) {
          dd.hideLoading();
          dd.alert({
            content: '未查询到相关数据,请重新查询!',
            buttonText: '确定'
          });
          return;
        }
        // dd.setStorage({
        //   key:'list',
        //   data:list
        // })
        that.setData({
          listData:{
            onItemTap:'onItemTap',
            data:[]
          }
        })
        that.setData({
          listData:{
            onItemTap:'onItemTap',
            data:list[0]
          }
        })
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
  onItemTap(e){
    var index = e.currentTarget.dataset.index;
    var sel_data;
    if (this.data.jd == '"kh"') {
      sel_data = this.data.listData.data[index].dwmc
      dd.confirm({
      title: '温馨提示',
      content: '您是否选择:'+sel_data,
      confirmButtonText: '确定',
      cancelButtonText: '重选',
      success: (result) => {
        if (result.confirm) {
          getApp().globalData.zwwldw = this.data.listData.data[index];
          dd.navigateBack({
            delta: 1
          });
        }
      },
    });
    } 
    else {
      var js =  this.data.listData.data[index].js
      if (js == 1) {
        var that = this;
        var url = '';
        var data;
        url='http://124.133.235.142:9020/lswlzd';
        data = JSON.stringify({
          "wlmc": '',
          "wlbh": '',
          'wllb': this.data.listData.data[index].wlbh
        })
          
        dd.httpRequest({
          headers: {
            "Content-Type": "application/json"
          },
          url: url,
          method: 'POST',
          data:data,
          dataType: 'json',
          success: function(res) {
            var list = [res.data];
            console.log(list);
            if (list[0].length <=0 ) {
              dd.hideLoading();
              dd.alert({
                content: '未查询到相关数据,请重新查询!',
                buttonText: '确定'
              });
              return;
            }
            // dd.setStorage({
            //   key:'list',
            //   data:list
            // })
            that.setData({
              listData:{
                onItemTap:'onItemTap',
                data:[]
              }
            })
            that.setData({
              listData:{
                onItemTap:'onItemTap',
                data:list[0]
              }
            })
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
      } else {
        sel_data = this.data.listData.data[index].wlmc
        this.setData({
          modalOpened: true,
          lswlmc:sel_data,
          wlindex:index
        });
      }
      
    }
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
      return;
    }
    this.data.listData.data[this.data.wlindex].sl = this.data.wlsl;
    this.setData({
      modalOpened: false
    });
    const app = getApp();
    var lswlzd = app.globalData.lswlzd;

    if (lswlzd.length == 0) {
      getApp().globalData.lswlzd.push(this.data.listData.data[this.data.wlindex]);
    } else {
      var count = 0;
      for (let index = 0; index < lswlzd.length; index++) {
        const element = lswlzd[index].wlbh;
        console.log(element)
        if (element == this.data.listData.data[this.data.wlindex].wlbh) {
          lswlzd[index].sl = lswlzd[index].sl  + this.data.listData.data[this.data.wlindex].sl;
          count = 1
        }
      }
      if (count == 0) {
        getApp().globalData.lswlzd.push(this.data.listData.data[this.data.wlindex]);
      }
    }
    dd.navigateBack({
      delta: 1
    });
  },
  onExtraTap(){
    this.onShow();
    return;
    var that = this;
    var url = '';
    var data;
    dd.scan({
      type: 'qr',
      success: (res) => {
        dd.alert({ title: res.code });
        url='http://124.133.235.142:9020/lswlzd';
        data = JSON.stringify({
          "wlmc": '',
          "wlbh": res.code,
          "wllb":''
        })
      
        dd.httpRequest({
          headers: {
            "Content-Type": "application/json"
          },
          url: url,
          method: 'POST',
          data:data,
          dataType: 'json',
          success: function(res) {
            var list = [res.data];
            if (list[0].length <=0 ) {
              dd.hideLoading();
              dd.alert({
                content: '未查询到相关数据,请重新查询!',
                buttonText: '确定'
              });
              return;
            }
            // dd.setStorage({
            //   key:'list',
            //   data:list
            // })
            that.setData({
              listData:{
                onItemTap:'onItemTap',
                data:[]
              }
            })
            that.setData({
              listData:{
                onItemTap:'onItemTap',
                data:list[0]
              }
            })
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
    });
  },
  onChangeSl(value){
    this.setData({
      wlsl: value,
    });
  },
  data: {
    wlsl:0,
    modalOpened: false,
    lswlmc:'',
    lastTapTime:0,
    jd:"",
    page:0,
    data: {
      list:[],
      listData:[]
    },
    inputValue:'',
    wlindex:0
  }
});
