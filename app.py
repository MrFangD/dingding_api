from flask import Flask, request
import requests, datetime
import os
import json
from Db_connection import Mssql
mssql = Mssql()

app = Flask(__name__)


#获取物料类别
@app.route('/getwllb', methods=['POST'])
def get_wllb():

    SQL = """SELECT LSWLLB_LBBH,LSWLLB_LBMC FROM LSWLLB  WHERE LSWLLB_MX = '1' AND LSWLLB_LBBH IN (SELECT LSWLZD_LBBH FROM LSWLZD 
            WHERE LSWLZD_SFFQ = '0' AND LSWLZD_C1 = '是') ORDER BY LSWLLB_LBBH"""
    reslist = mssql.execQuery(SQL)
    wllb = []
    for i in reslist:
        text={'wlmc':i[1], 'wlbh':i[0], 'checkvalue': -1, 'sl': 0, 'js':1}
        wllb.append(text)
    return json.dumps(wllb, ensure_ascii=False, indent=4)


# 物料字典接口
@app.route('/lswlzd', methods=['POST'])
def get_lswlxx():
    wlmc = request.json.get('wlmc')
    wlbh = request.json.get('wlbh')
    wllb = request.json.get('wllb')
    SQL = "SELECT LSWLZD_WLMC,LSWLZD_wlbh,LSWLZD_GGXH,JSJLDW_DWMC FROM LSWLZD,JSJLDW WHERE JSJLDW_DWDM = LSWLZD_JLDW AND  LSWLZD_WLBH LIKE '%"+wlbh+"%' AND LSWLZD_WLMC LIKE '%"+wlmc+"%' AND LSWLZD_SFFQ = '0' AND LSWLZD_C1 = '是' AND LSWLZD_LBBH LIKE '"+wllb+"%' ORDER BY LSWLZD_WLBH"
    reslist = mssql.execQuery(SQL)
    print(SQL)
    wlzd = []
    for i in reslist:
        text={'wlmc':i[0], 'wlbh':i[1], 'checkvalue': -1, 'sl': 0, 'js':0, 'ggxh':i[2], 'jlmc':i[3]}
        wlzd.append(text)
    return json.dumps(wlzd, ensure_ascii=False, indent=4)


# 往来单位接口
@app.route('/zwwldw', methods=['POST'])
def get_wldw():
    dwmc = request.json.get('dwmc')
    sql = "select ZWWLDW_DWbh,ZWWLDW_DWmc from ZWWLDW where ZWWLDW_DWmc like '%"+dwmc+"%'"
    reslist = mssql.execQuery(sql)
    zwdw = []
    for i in reslist:
        text = {'dwbh': i[0], 'dwmc': i[1], 'checkvalue': 1}
        zwdw.append(text)
    return json.dumps(zwdw, ensure_ascii=False, indent=4)


# 处理销售订单
@app.route('/xsdd', methods=['POST'])
def set_xsdd():
    khbh = request.json.get('khbh')
    khmc = request.json.get('khmc')
    zgxm = request.json.get('zgxm')
    ywrq = request.json.get('ywrq')
    ywrq = str(datetime.datetime.strptime(ywrq.replace('/', '-'), '%Y-%m-%d').date())
    btxx_list = request.json.get('btxx')
    bz = request.json.get('bz')
    ywlx = request.json.get('ywlx')
    fllx = 'BZXM'
    #处理业务类型
    if ywlx =='现款销售':
        ywlx ='01'
    elif ywlx =='正常销售':
        ywlx = '03'
    elif ywlx =='免费':
        ywlx = '25'
        fllx = 'MFXM'
    bmbh=''
    rybh=''
    # TODO:获取人员编号
    zwzgzd_sql = "SELECT ZWZGZD_ZGBH,ZWZGZD_ZGXM,ZWZGZD_BMBH FROM ZWZGZD WHERE ZWZGZD_ZGXM = '%s'" %zgxm
    print('职工姓名', zgxm)
    zgzd_list = mssql.execQueryLsh(zwzgzd_sql)
    for zgzd in zgzd_list:
        bmbh = zgzd[2]
        rybh = zgzd[0]
        print('职工部门', bmbh)
        print('职工编号', rybh)

    #处理单据流水以及单据编号
    djbh_list = mssql.execQueryLsh(f"exec get_djbh")
    for djbh in djbh_list:
        djls = djbh[0]
        djbh = djbh[1]
    # 处理表头
    xsdd_sql= """INSERT INTO XSDD(
        XSDD_DDLS, XSDD_DDZT, XSDD_DDBZ, XSDD_YWBH, XSDD_PJLX, XSDD_YWBS, XSDD_DDBH,
        XSDD_YWRQ, XSDD_DJRQ, XSDD_QCBZ, XSDD_SHDKH, XSDD_SHDKHMC, XSDD_SODKH, XSDD_SODKHMC, XSDD_SPKH, XSDD_SPKHMC,
        XSDD_FKKH, XSDD_FKKHMC,XSDD_WBBH, XSDD_HL, XSDD_BMBH, XSDD_RYBH, XSDD_ZDXM, XSDD_SHBZ,XSDD_BZ)
    VALUES ('%s','0','LD','%s','BZYWDD','S','%s',
    '%s','%s','0','%s','%s','%s','%s','%s','%s',
    '%s','%s','RMB',1,'%s','%s','%s','0','%s')""" % (djls,ywlx, djbh, ywrq.replace('-', ''), ywrq.replace('-', ''),khbh,khmc,khbh,khmc,khbh,khmc,khbh,khmc,bmbh,rybh,zgxm,bz )
    dd_return = mssql.execNonQuery(xsdd_sql)

    if not dd_return:
        return {'info': '表头数据保存失败!'}
    i = 1
    for btxx in btxx_list:
        # 获取辅助数量
        jl_sql = "SELECT LSWLZD_JLDW,LSWLZD_FZDW,LSWLZD_CCCK FROM LSWLZD WHERE LSWLZD_WLBH = '%s'" %btxx['wlbh']
        jl_list = mssql.execQuery(jl_sql)
        for jl in jl_list:
            zjl = jl[0]
            fjl = jl[1]
            ckbh = jl[2]
            if jl[2] in ('01','02'):
                ckbh = '01'
            if zjl == fjl:
                fsl = btxx['sl']
            else:
                hsxs_sql = "SELECT JSJLDWHS_XS2 FROM JSJLDWHS WHERE JSJLDWHS_DWDM1 = '%s' AND JSJLDWHS_DWDM2='%s'" %(jl[1], jl[0])
                hsxs_list = mssql.execQuery(hsxs_sql)
                for hsxs in hsxs_list:
                    if hsxs[0] == 0:
                        fsl = btxx['sl']
                    else:
                        fsl = round(btxx['sl'] / hsxs[0], 2)
        # 根据物料、单位获取价格政策
        # JJZC_SQL ="""SELECT XSDWWLGX_YZHSJ, XSDWWLGX_YZXSJ FROM XSDWWLGX WHERE XSDWWLGX_DWBH = '%s'
        #             AND XSDWWLGX_WLBH = '%s' AND XSDWWLGX_WBBH = 'RMB' AND XSDWWLGX_PJLX = 'BZYWDD'""" %(khbh, btxx['wlbh'])
        # JJZC_list = mssql.execQuery(JJZC_SQL)
        jj = get_price(btxx['wlbh'], khbh, ywrq.replace('-', ''), rybh)
        if not jj:
            jj = 100
        if ywlx == "25":
            jj = 0
        zjj = jj * btxx['sl']
        xsdd_ddfl = '0'
        xsdd_ddfl = xsdd_ddfl*(10-len(str(i)))
        xsddfl = xsdd_ddfl+str(i)
        # 处理表体sql
        xsddmx_sql ="""INSERT INTO XSDDMX(XSDDMX_DDLS, XSDDMX_DDFL, XSDDMX_FLLX, XSDDMX_WLBH,
                XSDDMX_ZSL,XSDDMX_FSL1, XSDDMX_FSL2,
                XSDDMX_YZHSJ, XSDDMX_YZXSJ, XSDDMX_BZHSJ, XSDDMX_BZXSJ, XSDDMX_YSE, XSDDMX_BSE,
                XSDDMX_SL, XSDDMX_YHSE, XSDDMX_BHSE, XSDDMX_YXSE, XSDDMX_BXSE, XSDDMX_SFKP,XSDDMX_SFTD, XSDDMX_KCFS, XSDDMX_JHRQ,xsddmx_ckbh)
                VALUES('%s','%s','%s','%s',
                %s,%s,%s,
                %s,%s,%s,%s,0,0,
                0, %s,%s,%s,%s,'1','1','PT','%s','%s'
                ) 
        """ %(djls, xsddfl, fllx, btxx['wlbh'], btxx['sl'], btxx['sl'], fsl,jj,jj,jj,jj,zjj,zjj,zjj,zjj,ywrq.replace('-', ''),ckbh)
        bt_return = mssql.execNonQuery(xsddmx_sql)
        if not bt_return:
            return {'info': '表体数据保存失败!'}
        i += 1
    return {'info': '数据保存成功!'}


# 获取销售订单列表
@app.route('/getxsddlist', methods=['POST'])
def get_xsddlsit():
    zdxm = request.json.get('zdr')
    xsdd_bt=[]
    xsdd_mx=[]
    xsdd_sql = """ SELECT XSDD_DJRQ,XSDD_DDBH,XSDD_SHDKHMC,XSDD_SHDKH,XSDD_DDLS, XSDD_SHBZ,XSDD_BZ 
            FROM XSDD WHERE XSDD_ZDXM = '%s' 
    """ % zdxm
    xsdd_list = mssql.execQuery(xsdd_sql)
    for xsdd in xsdd_list:
        xsdd_mx=[]
        if xsdd[5] == '1':
            xsddbt = {'djrq': xsdd[0], 'djbh': xsdd[1], 'khmc': xsdd[2], 'khbh': xsdd[3], 'lsbh': xsdd[4],
                      'djzt': '已审批','bz':xsdd[6]}
        else:
            xsddbt = {'djrq': xsdd[0], 'djbh': xsdd[1], 'khmc': xsdd[2],'khbh':xsdd[3],'lsbh':xsdd[4], 'djzt': '未审批','bz':xsdd[6]}
        xsddmx_sql = """SELECT LSWLZD_WLBH, LSWLZD_WLMC, XSDDMX_ZSL FROM XSDDMX, LSWLZD WHERE LSWLZD_WLBH = XSDDMX_WLBH AND XSDDMX_DDLS = '%s'""" %xsdd[4]
        print(xsddmx_sql)
        xsddmx_list = mssql.execQuery(xsddmx_sql)
        for xsddmx in xsddmx_list:
            xsddmx = {'wlbh':xsddmx[0],'wlmc':xsddmx[1], 'sl':xsddmx[2]}
            print(xsddmx)
            xsdd_mx.append(xsddmx)
        xsddbt["xsddmx"]=xsdd_mx
        xsdd_bt.append(xsddbt)
    print(xsdd_bt)
    return json.dumps(xsdd_bt, ensure_ascii=False, indent=4)


# 删除销售订单
@app.route('/delxsdd', methods=['POST'])
def del_xsdd():
    lsbh = request.json.get('lsbh')
    print(lsbh)
    del_xsdd_sql ="DELETE FROM XSDD WHERE XSDD_DDLS = '%s'" %lsbh
    bt_return = mssql.execNonQuery(del_xsdd_sql)
    if not bt_return:
        return {'info': '表体数据删除失败!'}
    del_xsddmx_sql = "DELETE FROM XSDDMX WHERE XSDDMX_DDLS = '%s'" % lsbh
    ddmx_return = mssql.execNonQuery(del_xsddmx_sql)
    if not ddmx_return:
        return {'info': '表体数据删除失败!'}
    return {'info': '数据删除成功!'}


# 更新销售订单
@app.route('/updxsdd', methods=['POST'])
def upd_xsdd():
    khbh = request.json.get('khbh')
    khmc = request.json.get('khmc')
    lsbh = request.json.get('lsbh')
    ywrq = request.json.get('ywrq')
    # ywrq = str(datetime.datetime.strptime(ywrq.replace('/', '-'), '%Y-%m-%d').date())
    btxx_list = request.json.get('btxx')
    ywlx = request.json.get('ywlx')
    bz = request.json.get('bz')

    print('业务类型',ywlx)
    fllx = 'BZXM'
    #处理业务类型
    if ywlx =='现款销售':
        ywlx ='01'
    elif ywlx =='正常销售':
        ywlx = '03'
    elif ywlx =='免费':
        ywlx = '25'
        fllx = 'MFXM'
    # 更新表头
    xsdd_sql = """UPDATE XSDD SET XSDD_SHDKH ='%s', XSDD_SHDKHMC='%s', 
                XSDD_SODKH='%s', XSDD_SODKHMC='%s', 
                XSDD_SPKH='%s', XSDD_SPKHMC='%s',
                XSDD_FKKH='%s', XSDD_FKKHMC='%s', XSDD_BZ = '%s',
                XSDD_YWBH ='%s', xsdd_sprq ='20211212'
                WHERE XSDD_DDLS ='%s'""" % (khbh, khmc, khbh, khmc, khbh, khmc, khbh, khmc,bz,ywlx,lsbh)
    print(xsdd_sql)
    dd_return = mssql.execNonQuery(xsdd_sql)
    if not dd_return:
        return {'info': '表头数据保存失败!'}

    # 对于表体先删除后插入
    del_ddmx_sql = """DELETE FROM XSDDMX WHERE XSDDMX_DDLS ='%s'""" %lsbh
    dd_return = mssql.execNonQuery(del_ddmx_sql)
    print(del_ddmx_sql)
    if not dd_return:
        return {'info': '表体数据删除失败!'}
    i=1
    print(btxx_list)
    rybh = ''
    # TODO:获取人员编号
    zwzgzd_sql = "SELECT XSDD_RYBH FROM XSDD WHERE XSDD_DDLS = '%s'" % lsbh
    zgzd_list = mssql.execQueryLsh(zwzgzd_sql)
    for zgzd in zgzd_list:
        rybh = zgzd[0]

    for btxx in btxx_list:
        # 获取辅助数量
        jl_sql = "SELECT LSWLZD_JLDW,LSWLZD_FZDW,LSWLZD_CCCK,substring(lswlzd_lbbh,0,3) FROM LSWLZD WHERE LSWLZD_WLBH = '%s'" % btxx['wlbh']
        jl_list = mssql.execQuery(jl_sql)
        for jl in jl_list:
            zjl = jl[0]
            fjl = jl[1]
            ckbh = jl[2]
            if jl[2] in ('01','02'):
                ckbh = '01'
            if zjl == fjl:
                fsl = btxx['sl']
            else:
                hsxs_sql = "SELECT JSJLDWHS_XS2 FROM JSJLDWHS WHERE JSJLDWHS_DWDM1 = '%s' AND JSJLDWHS_DWDM2='%s'" % (
                jl[1], jl[0])
                hsxs_list = mssql.execQuery(hsxs_sql)
                for hsxs in hsxs_list:
                    if hsxs[0] == 0:
                        fsl = btxx['sl']
                    else:
                        fsl = round(btxx['sl'] / hsxs[0], 2)
        # 根据物料、单位获取价格政策
        jj = get_price(btxx['wlbh'], khbh, ywrq, rybh)
        if not jj:
            jj = 100
        if ywlx == "25":
            jj = 0
        zjj = jj * btxx['sl']
        xsdd_ddfl = '0'
        xsdd_ddfl = xsdd_ddfl * (10 - len(str(i)))
        xsddfl = xsdd_ddfl + str(i)
        # 处理表体sql
        xsddmx_sql = """INSERT INTO XSDDMX(XSDDMX_DDLS, XSDDMX_DDFL, XSDDMX_FLLX, XSDDMX_WLBH,
                XSDDMX_ZSL,XSDDMX_FSL1, XSDDMX_FSL2,
                XSDDMX_YZHSJ, XSDDMX_YZXSJ, XSDDMX_BZHSJ, XSDDMX_BZXSJ, XSDDMX_YSE, XSDDMX_BSE,
                XSDDMX_SL, XSDDMX_YHSE, XSDDMX_BHSE, XSDDMX_YXSE, XSDDMX_BXSE, XSDDMX_SFKP,XSDDMX_SFTD, XSDDMX_KCFS, XSDDMX_JHRQ,xsddmx_ckbh)
                VALUES('%s','%s','%s','%s',
                %s,%s,%s,
                %s,%s,%s,%s,0,0,
                0, %s,%s,%s,%s,'1','1','PT','%s','%s'
                ) 
        """ % (lsbh, xsddfl,fllx, btxx['wlbh'], btxx['sl'], btxx['sl'], fsl, jj, jj, jj, jj, zjj, zjj, zjj, zjj, ywrq,ckbh)
        bt_return = mssql.execNonQuery(xsddmx_sql)
        if not bt_return:
            return {'info': '表体数据保存失败!'}
        i += 1
    return {'info': '数据保存成功!'}


@app.route('/hello')
def say_hells():
    return 'hello'

# 获取用户信息
@app.route('/getuser', methods=['POST'])
def get_user():
    code_get = request.json.get('code')
    print(code_get)
    # 获取access_token
    AppKey = 'ding0o0n8grewoohq4ie'
    AppSecret = '3Iglyg5Uv6Vpmv7_TtaQHK6eLp28i3H3zDE3RFMNS14bADjwP4AJu3yZOP9k3xND'
    access_token_url = 'https://oapi.dingtalk.com/gettoken'
    params = {'appkey': AppKey, 'appsecret': AppSecret}
    req_access_token = requests.get(url=access_token_url, params=params)
    # print(req_access_token.text)
    req_access_token_json = json.loads(req_access_token.text)
    # print(req_access_token_json["access_token"])
    # 获取用户userid
    access_token = req_access_token_json["access_token"]
    code = code_get
    access_token_url = 'https://oapi.dingtalk.com/user/getuserinfo'
    params = {'access_token': access_token, 'code': code}
    req_userid = requests.get(url=access_token_url, params=params)
    req_userid_json = json.loads(req_userid.text)
    # print(req_userid_json)
    # print(req_userid_json["userid"])
    # 获取用户详情
    print(req_userid_json)
    userid = req_userid_json["userid"]
    access_token_url = 'https://oapi.dingtalk.com/user/get'
    params = {'access_token': access_token, 'userid': userid}
    req_mx = requests.get(url=access_token_url, params=params)
    req_mx_json = json.loads(req_mx.text)
    # print(req_mx_json)
    return req_mx.text

# 获取价格政策
def get_price(pswlbh, psDW,psywrq,pszgbh):
    jgys_sql = """SELECT XSJGYS_LSBH, XSJGYS_WLLB, XSJGYS_CPZ, XSJGYS_WLBH,XSJGYS_DWLB, XSJGYS_KHZ, XSJGYS_DQ, XSJGYS_DWBH, XSJGYS_ZGBH,
            XSJGYS_YWLX, XSJGYS_RQ, XSJGYS_SL, XSJGYS_YSFS, XSJGYS_ZYX, XSJGYS_YXJ
            FROM XSJGYS """

    jgys_list = mssql.execQuery(jgys_sql)
    for jgys in jgys_list:
        vsysWLLB = jgys[1]
        vsysCPZ = jgys[2]
        vsysWLBH = jgys[3]
        vsysDWLB = jgys[4]
        vsysKHZ = jgys[5]
        vsysDQ = jgys[6]
        vsysDWBH = jgys[7]
        vsysZGBH = jgys[8]
        vsysYWLX = jgys[9]
        vsysRQ = jgys[10]
        vsysSL = jgys[11]
        vsysYSFS = jgys[12]
        vsysZYX = jgys[13]
        kcje_jg =[]
        vsSQL = """SELECT XSJGMX_DWLB, round(100 - XSJGMX_ZKJE,4),XSJGMX_JSRQ
                    FROM XSJGMX,XSJGZC WHERE XSJGMX_ZCLS = XSJGZC_ID AND XSJGZC_ZT = '1' """

        # 人员编号
        if vsysZGBH == '1':
            vsSQL += " AND  XSJGMX_ZGBH = '" + pszgbh + "'"

        # // 如果有了物料编号，产品组和物料类别不用考虑
        # // 时间: 小于等于结束日期，大于等于开始日期
        if vsysRQ == '1':
            vsSQL += "  AND XSJGMX_KSRQ <='" + psywrq + "' AND XSJGMX_JSRQ >='" + psywrq+"'"
        if vsysWLBH == '1':
            vsSQL += " AND XSJGMX_WLBH = '" + pswlbh + "' "
        else:
            # // 产品组: 如果产品为空，就不能使用产品组这个政策
            if vsysCPZ == '1':
                vsCPZ = ''
            # // 物料类别
            if vsysWLLB == '1':
                vsWLLB = ''
                WLLB_SQL ="SELECT LSWLZD_LBBH from LSWLZD WHERE LSWLZD_WLBH ='%s'" % pswlbh
                wllb_list = mssql.execQuery(WLLB_SQL)
                for wllb in wllb_list:
                    vsWLLB1 = wllb[0]
                vsSQL += " XSJGMX_WLLB in (" + vsWLLB1 + ") AND"

        # // 如果有了往来单位，客户组和单位类别地区就不用考虑
        if vsysDWBH == '1':
            vsSQL += "  AND XSJGMX_DWBH = '" + psDW + "' "
        else:
            # // 单位类别
            if vsysDWLB =='1':
                vsDWLB_old = ''
                dwlb_sql = "SELECT ZWWLDW_LBBH from ZWWLDW WHERE ZWWLDW_DWBH ='%s'" %psDW
                dwlb_list = mssql.execQuery(dwlb_sql)
                for dwlb in dwlb_list:
                    vsDWLB_old = dwlb[0]
                vsDWLB = struct(vsDWLB_old)
                vsSQL += " and  XSJGMX_DWLB in " + vsDWLB

        vsSQL_list = mssql.execQuery(vsSQL)
        for vsjgzc in vsSQL_list:
            kcje_jg.append(vsjgzc)
            # vs_dwlb = vsjgzc[0]
            # zkle = vsjgzc[1]
        #判断单位类别是否最接近
        jg_list = []
        for dw in kcje_jg:
            dw_ywrq = dw[2]
            if dw[2].replace(" ", "") == "":
                dw_ywrq = "99999999"
            if dw_ywrq >= psywrq:
                if dw_ywrq =="99999999":
                    dw_ywrq = "00000000"
                tuple = (dw[0],dw_ywrq,dw[1])
                jg_list.append(tuple)
            else:
                continue
        if len(jg_list) >0:
            jg = max(jg_list)
            return jg[2]


def struct(psstr):
    k = 0
    i = 0
    psStru = "222322"
    vsReturn = ""
    while i < len(psStru):
        k = k + int(psStru[i:i+1])
        if i == len(psStru)-1:
            vsReturn = vsReturn + "'" + psstr[0:k] + "'"
        else:
            vsReturn = vsReturn + "'" + psstr[0:k] + "',"
        i +=1
    vsReturn = "(" + vsReturn + ")"
    return vsReturn

def stru(psstr,pslb):
    if pslb in psstr:
        psstru = "222322"
        viLen = len(psstru)
        viLBLen = len(pslb)
        k = 0
        i = 0
        while i < viLen:
            k = k + int(psstru[i:i+1])
            if k == viLBLen:
                return i
            i += 1
    else:
        return 0


if __name__ == '__main__':
    app.run(host='192.168.1.9', port=5000, debug=True)
