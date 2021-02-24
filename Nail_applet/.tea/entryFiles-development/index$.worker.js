if(!self.__appxInited) {
self.__appxInited = 1;


require('./config$');


      if( navigator.userAgent && (navigator.userAgent.indexOf('LyraVM') > 0 || navigator.userAgent.indexOf('AlipayIDE') > 0) ) {
        var AFAppX = self.AFAppX.getAppContext ? self.AFAppX.getAppContext().AFAppX : self.AFAppX;
      } else {
        importScripts('https://appx/af-appx.worker.min.js');
        var AFAppX = self.AFAppX;
      }
      self.getCurrentPages = AFAppX.getCurrentPages;
      self.getApp = AFAppX.getApp;
      self.Page = AFAppX.Page;
      self.App = AFAppX.App;
      self.my = AFAppX.bridge || AFAppX.abridge;
      self.abridge = self.my;
      self.Component = AFAppX.WorkerComponent || function(){};
      self.$global = AFAppX.$global;
      self.requirePlugin = AFAppX.requirePlugin;
    

if(AFAppX.registerApp) {
  AFAppX.registerApp({
    appJSON: appXAppJson,
  });
}



function success() {
require('../../app');
require('../../node_modules/mini-ali-ui/es/loading/index?hash=05d2a9730dd6009bf9446182f9c985f40f8c0f43');
require('../../node_modules/mini-ali-ui/es/button/index?hash=e1617a0257fb9de746f60d50b03404ad924976c9');
require('../../node_modules/mini-ali-ui/es/am-icon/index?hash=05d2a9730dd6009bf9446182f9c985f40f8c0f43');
require('../../node_modules/mini-ali-ui/es/modal/index?hash=febd4c40992222524e0db12a74760a28f8f9b339');
require('../../node_modules/mini-ali-ui/es/stepper/index?hash=5a0c180d5ccf7c9d483dd4817cdab5489824013c');
require('../../node_modules/mini-ali-ui/es/swipe-action/index?hash=05d2a9730dd6009bf9446182f9c985f40f8c0f43');
require('../../node_modules/mini-ali-ui/es/list/index?hash=e1617a0257fb9de746f60d50b03404ad924976c9');
require('../../node_modules/mini-ali-ui/es/list/auto-size-img/index?hash=05d2a9730dd6009bf9446182f9c985f40f8c0f43');
require('../../node_modules/mini-ali-ui/es/list/list-item/index?hash=a5465b8c889360e3f854461d3ac41cf414aec633');
require('../../node_modules/mini-ali-ui/es/input-item/index?hash=5a0c180d5ccf7c9d483dd4817cdab5489824013c');
require('../../node_modules/mini-ali-ui/es/picker-item/index?hash=5a0c180d5ccf7c9d483dd4817cdab5489824013c');
require('../../node_modules/mini-ali-ui/es/tag/index?hash=5a0c180d5ccf7c9d483dd4817cdab5489824013c');
require('../../pages/index/index?hash=21eb644197289e3269a8f2a097fb762da396100f');
require('../../pages/xsorder_list/order_list?hash=22bfdb0412807fb366afc807e02ca77ad7fa5443');
require('../../pages/zwdw/zwdw?hash=21a435a974a40b3e575322739d94848f578bc3e5');
require('../../pages/delxsdd/index?hash=39773082dea66a72516f77a6b47f55a25c4a278b');
}
self.bootstrapApp ? self.bootstrapApp({ success }) : success();
}