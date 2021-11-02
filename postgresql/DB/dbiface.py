'''
    Author: Chandra Krintz, UCSB, ckrintz@cs.ucsb.edu, AppScale BSD license
    USAGE: python dbiface.py 169.231.XXX.YYY table_name postgres_user_name password
'''
import psycopg2, sys, argparse
from datetime import datetime, date, timedelta
from dateutil.relativedelta import relativedelta

DEBUG=False

TABLE_TYPE_MAP = {
    'meas':""" (dt timestamp PRIMARY KEY, 
        meas real
    )
    """,
    'temp':""" (dt timestamp PRIMARY KEY, 
        temp real 
    )
    """,
    'image':""" (fname varchar(128) PRIMARY KEY, 
	dt timestamp,	
        size real,
        camera varchar(32),
        fullpath varchar(128)
    )
    """,
    'imageblob':""" (fname varchar(128) PRIMARY KEY, 
	dt timestamp,	
        size real,
        camera varchar(32),
        fullpath varchar(128),
	exifblob varchar(4096)
    )
    """,
    'cimis':""" (dt timestamp PRIMARY KEY, 
        temp real, 
        hum real, 
        vappres real,
        dewpt real,
        solrad real,
        netrad real,
        eto real,
        a_eto real,
        a_etr real,
        precip real,
        windres real,
        winddir real,
        windspd real,
        soil real 
    )
    """,
    'flex':""" (dt timestamp PRIMARY KEY, 
        temp5ft real, 
        hum real, 
        temp30ft real,
        dewpoint real,
        winddir varchar(8),
        windspd real,
        precip real
    )
    """ ,
    'pred':""" (dt timestamp PRIMARY KEY, 
        gtmeas real,
        estdt timestamp,
        estmeas real,
        pred real
    )
    """,
    'simple':""" (dt timestamp PRIMARY KEY, 
        meas real
    )
    """,
    'simple2':""" (dt timestamp PRIMARY KEY, 
        meas real,
        meas2 real
    )
    """,
    'simplestr':""" (dt timestamp PRIMARY KEY, 
        meas varchar(512)
    )
    """,
    'simple3':""" (dt timestamp PRIMARY KEY, 
        meas real,
        meas2 real,
        meas3 real
    )
    """,
    'status':""" (dt timestamp PRIMARY KEY, 
        TimeStamp timestamp,
        Record bigint,
        OSVersion varchar(32),
        OSDate varchar(32),
        OSSignature real,
        SerialNumber varchar(32),
        RevBoard varchar(32),
        StationName varchar(32),
        PakBusAddress real,
        ProgName varchar(32),
        StartTime timestamp,
        RunSignature real,
        ProgSignature real,
        Battery real,
        PanelTemp real,
        WatchdogErrors real,
        LithiumBattery real,
        Low12VCount real,
        Low5VCount real,
        CompileResults varchar(256),
        StartUpCode real,
        ProgErrors real,
        VarOutOfBound real,
        SkippedScan real,
        SkippedSystemScan real,
        SkippedSlowScan real,
        ErrorCalib real,
        MemorySize real,
        MemoryFree real,
        CPUDriveFree real,
        USRDriveFree real,
        CommsMemFree1 real,
        CommsMemFree2 real,
        CommsMemFree3 real,
        FullMemReset real,
        DataTableName1 varchar(32),
        DataTableName2 varchar(32),
        DataTableName3 varchar(32),
        DataTableName4 varchar(32),
        DataTableName5 varchar(32),
        DataTableName6 varchar(32),
        DataTableName7 varchar(32),
        DataTableName8 varchar(32),
        DataTableName9 varchar(32),
        DataTableName10 varchar(32),
        SkippedRecord1 real,
        SkippedRecord2 real,
        SkippedRecord3 real,
        SkippedRecord4 real,
        SkippedRecord5 real,
        SkippedRecord6 real,
        SkippedRecord7 real,
        SkippedRecord8 real,
        SkippedRecord9 real,
        SkippedRecord10 real,
        DataRecordSize1_1 real,
        DataRecordSize1_2 real,
        DataRecordSize2_1 real,
        DataRecordSize2_2 real,
        DataRecordSize3_1 real,
        DataRecordSize3_2 real,
        DataRecordSize4_1 real,
        DataRecordSize4_2 real,
        DataRecordSize5_1 real,
        DataRecordSize5_2 real,
        DataRecordSize6_1 real,
        DataRecordSize6_2 real,
        DataRecordSize7_1 real,
        DataRecordSize7_2 real,
        DataRecordSize8_1 real,
        DataRecordSize8_2 real,
        DataRecordSize9_1 real,
        DataRecordSize9_2 real,
        DataRecordSize10_1 real,
        DataRecordSize10_2 real,
        SecsPerRecord1 real,
        SecsPerRecord2 real,
        SecsPerRecord3 real,
        SecsPerRecord4 real,
        SecsPerRecord5 real,
        SecsPerRecord6 real,
        SecsPerRecord7 real,
        SecsPerRecord8 real,
        SecsPerRecord9 real,
        SecsPerRecord10 real,
        DataFillDays1_1 real,
        DataFillDays1_2 real,
        DataFillDays2_1 real,
        DataFillDays2_2 real,
        DataFillDays3_1 real,
        DataFillDays3_2 real,
        DataFillDays4_1 real,
        DataFillDays4_2 real,
        DataFillDays5_1 real,
        DataFillDays5_2 real,
        DataFillDays6_1 real,
        DataFillDays6_2 real,
        DataFillDays7_1 real,
        DataFillDays7_2 real,
        DataFillDays8_1 real,
        DataFillDays8_2 real,
        DataFillDays9_1 real,
        DataFillDays9_2 real,
        DataFillDays10_1 real,
        DataFillDays10_2 real,
        CardStatus varchar(256),
        CardBytesFree real,
        MeasureOps real,
        MeasureTime real,
        ProcessTime real,
        MaxProcTime real,
        BuffDepth real,
        MaxBuffDepth real,
        LastSystemScan timestamp,
        LastSlowScan timestamp,
        SystemProcTime real,
        SlowProcTime real,
        MaxSystemProcTime real,
        MaxSlowProcTime real,
        PortStatus1 boolean,
        PortStatus2 boolean,
        PortStatus3 boolean,
        PortStatus4 boolean,
        PortStatus5 boolean,
        PortStatus6 boolean,
        PortStatus7 boolean,
        PortStatus8 boolean,
        PortConfig1 varchar(32),
        PortConfig2 varchar(32),
        PortConfig3 varchar(32),
        PortConfig4 varchar(32),
        PortConfig5 varchar(32),
        PortConfig6 varchar(32),
        PortConfig7 varchar(32),
        PortConfig8 varchar(32),
        SW12Volts1 boolean,
        SW12Volts2 boolean,
        Security1 real,
        Security2 real,
        Security3 real,
        RS232Power boolean,
        RS232Handshaking real,
        RS232Timeout real,
        CommActiveRS232 boolean,
        CommActiveME boolean,
        CommActiveCOM310 boolean,
        CommActiveSDC7 boolean,
        CommActiveSDC8 boolean,
        CommActiveCOM320 boolean,
        CommActiveSDC10 boolean,
        CommActiveSDC11 boolean,
        CommActiveCOM1 boolean,
        CommActiveCOM2 boolean,
        CommActiveCOM3 boolean,
        CommActiveCOM4 boolean,
        CommConfigRS232 real,
        CommConfigME real,
        CommConfigCOM310 real,
        CommConfigSDC7 real,
        CommConfigSDC8 real,
        CommConfigCOM320 real,
        CommConfigSDC10 real,
        CommConfigSDC11 real,
        CommConfigCOM1 real,
        CommConfigCOM2 real,
        CommConfigCOM3 real,
        CommConfigCOM4 real,
        BaudrateRS232 real,
        BaudrateME real,
        BaudrateSDC real,
        BaudrateCOM1 real,
        BaudrateCOM2 real,
        BaudrateCOM3 real,
        BaudrateCOM4 real,
        IsRouter boolean,
        PakBusNodes real,
        CentralRouters1 real,
        CentralRouters2 real,
        CentralRouters3 real,
        CentralRouters4 real,
        CentralRouters5 real,
        CentralRouters6 real,
        CentralRouters7 real,
        CentralRouters8 real,
        BeaconRS232 real,
        BeaconME real,
        BeaconSDC7 real,
        BeaconSDC8 real,
        BeaconSDC10 real,
        BeaconSDC11 real,
        BeaconCOM1 real,
        BeaconCOM2 real,
        BeaconCOM3 real,
        BeaconCOM4 real,
        VerifyRS232 real,
        VerifyME real,
        VerifySDC7 real,
        VerifySDC8 real,
        VerifySDC10 real,
        VerifySDC11 real,
        VerifyCOM1 real,
        VerifyCOM2 real,
        VerifyCOM3 real,
        VerifyCOM4 real,
        MaxPacketSize real,
        USRDriveSize real,
        IPInfo varchar(128),
        IPAddressEth varchar(128),
        IPMaskEth varchar(128),
        IPGateway varchar(128),
        TCPPort real,
        pppInterface real,
        pppIPAddr varchar(128),
        pppUsername varchar(32),
        pppPassword varchar(32),
        pppDial varchar(32),
        pppDialResponse varchar(32),
        IPTrace real,
        Messages varchar(32),
        CalVolts1 real,
        CalVolts2 real,
        CalVolts3 real,
        CalVolts4 real,
        CalVolts5 real,
        CalVolts6 real,
        CalVolts7 real,
        CalVolts8 real,
        CalVolts9 real,
        CalVolts10 real,
        CalVolts11 real,
        CalVolts12 real,
        CalVolts13 real,
        CalVolts14 real,
        CalVolts15 real,
        CalGain1 real,
        CalGain2 real,
        CalGain3 real,
        CalGain4 real,
        CalGain5 real,
        CalGain6 real,
        CalGain7 real,
        CalGain8 real,
        CalGain9 real,
        CalGain10 real,
        CalGain11 real,
        CalGain12 real,
        CalGain13 real,
        CalGain14 real,
        CalGain15 real,
        CalSeOffset1 real,
        CalSeOffset2 real,
        CalSeOffset3 real,
        CalSeOffset4 real,
        CalSeOffset5 real,
        CalSeOffset6 real,
        CalSeOffset7 real,
        CalSeOffset8 real,
        CalSeOffset9 real,
        CalSeOffset10 real,
        CalSeOffset11 real,
        CalSeOffset12 real,
        CalSeOffset13 real,
        CalSeOffset14 real,
        CalSeOffset15 real,
        CalDiffOffset1 real,
        CalDiffOffset2 real,
        CalDiffOffset3 real,
        CalDiffOffset4 real,
        CalDiffOffset5 real,
        CalDiffOffset6 real,
        CalDiffOffset7 real,
        CalDiffOffset8 real,
        CalDiffOffset9 real,
        CalDiffOffset10 real,
        CalDiffOffset11 real,
        CalDiffOffset12 real,
        CalDiffOffset13 real,
        CalDiffOffset14 real,
        CalDiffOffset15 real,
        IxResistor real,
        CAOOffset1 real,
        CAOOffset2 real
    )
    """,
    'fluxdata':""" (dt timestamp PRIMARY KEY, 
        TimeStamp timestamp,
        Record bigint,
        Hs real,
        tau real,
        u_star real,
        Ts_stdev real,
        Ts_Ux_cov real,
        Ts_Uy_cov real,
        Ts_Uz_cov real,
        Ux_stdev real,
        Ux_Uy_cov real,
        Ux_Uz_cov real,
        Uy_stdev real,
        Uy_Uz_cov real,
        Uz_stdev real,
        wnd_spd real,
        rslt_wnd_spd real,
        wnd_dir_sonic real,
        std_wnd_dir real,
        wnd_dir_compass real,
        Ux_Avg real,
        Uy_Avg real,
        Uz_Avg real,
        Ts_Avg real,
        sonic_azimuth real,
        sonic_samples_Tot real,
        no_sonic_head_Tot real,
        no_new_sonic_data_Tot real,
        amp_l_f_Tot real,
        amp_h_f_Tot real,
        sig_lck_f_Tot real,
        del_T_f_Tot real,
        aq_sig_f_Tot real,
        sonic_cal_err_f_Tot real,
        Fc real,
        LE real,
        Hc real,
        CO2_stdev real,
        CO2_Ux_cov real,
        CO2_Uy_cov real,
        CO2_Uz_cov real,
        H2O_stdev real,
        H2O_Ux_cov real,
        H2O_Uy_cov real,
        H2O_Uz_cov real,
        Tc_stdev real,
        Tc_Ux_cov real,
        Tc_Uy_cov real,
        Tc_Uz_cov real,
        CO2_mean real,
        H2O_mean real,
        cell_tmpr_mean real,
        cell_press_mean real,
        amb_press_mean real,
        Tc_mean real,
        rho_a_mean real,
        diff_press_Avg real,
        Td_Avg real,
        factor_CO2 real,
        factor_H2O real,
        irga_samples_Tot real,
        no_irga_head_Tot real,
        no_new_irga_data_Tot real,
        irga_bad_data_f_Tot real,
        a_fault_f_Tot real,
        irga_startup_f_Tot real,
        motor_spd_f_Tot real,
        tec_tmpr_f_Tot real,
        src_pwr_f_Tot real,
        src_tmpr_f_Tot real,
        src_curr_f_Tot real,
        irga_off_f_Tot real,
        irga_sync_f_Tot real,
        cell_tmpr_f_Tot real,
        cell_press_f_Tot real,
        CO2_I_f_Tot real,
        CO2_Io_f_Tot real,
        H2O_I_f_Tot real,
        H2O_Io_f_Tot real,
        CO2_Io_var_f_Tot real,
        H2O_Io_var_f_Tot real,
        CO2_sig_strgth_f_Tot real,
        H2O_sig_strgth_f_Tot real,
        htr_ctrl_off_f_Tot real,
        diff_press_f_Tot real,
        CO2_sig_strgth_mean real,
        H2O_sig_strgth_mean real,
        pump_tmpr_Avg real,
        pump_press_Avg real,
        pump_flow_duty_cycle_Avg real,
        pump_flow_Avg real,
        pump_flow_Std real,
        pump_flow_set_pt real,
        pump_heater_Avg real,
        pump_fan_Avg real,
        pump_off_Avg real,
        valve_tmpr_Avg real,
        valve_heater_Avg real,
        valve_fan_Avg real,
        intake_heater_Avg real,
        panel_tmpr_Avg real,
        batt_volt_Avg real,
        process_time_Avg real,
        process_time_Max real,
        buff_depth_Avg real,
        buff_depth_Max real,
        slowsequence_Tot real
    )
    """, #3rd to last in public can be NAN (real)
    'public':""" (dt timestamp PRIMARY KEY, 
        TimeStamp timestamp,
        Record bigint,
        system_diag real,
        panel_tmpr real,
        batt_volt real,
        set_press_source_flg boolean,
        press_source real,
        do_zero_flg boolean,
        do_CO2_span_flg boolean,
        do_H2O_span_flg boolean,
        ec155_off_flg boolean,
        sonic_azimuth real,
        Ux real,
        Uy real,
        Uz real,
        Ts real,
        diag_sonic real,
        CO2 real,
        H2O real,
        diag_irga real,
        cell_tmpr real,
        cell_press real,
        CO2_sig_strgth real,
        H2O_sig_strgth real,
        diff_press real,
        calib_type real,
        amb_press real,
        Tc real,
        Td real,
        pump_tmpr real,
        pump_press real,
        pump_flow real,
        pump_flow_set_pt real,
        pump_flow_duty_cycle real,
        mode real,
        sec_in_mode real,
        CO2_span_gas real,
        Td_span_gas real,
        H2O_span_gas real,
        valve_manual_tmpr_ctrl_flg boolean,
        valve_tmpr real,
        valve_diff_press_offset real,
        valve_ctrl_press real,
        valve_flow real,
        valve_flow_set_pt real,
        valve_flow_duty_cycle real,
        valve_auto_tmpr_ctrl_f boolean,
        lws real,
        intake_heater_power real,
        intake_heater_volts real
    )
    """,
    'tsdata':""" (dt timestamp PRIMARY KEY, 
        TimeStamp timestamp,
        Record bigint,
        Ux real,
        Uy real,
        Uz real,
        Ts real,
        diag_sonic real,
        CO2 real,
        H2O real,
        diag_irga real,
        cell_tmpr real,
        cell_press real,
        CO2_sig_strgth real,
        H2O_sig_strgth real,
        diff_press real,
        pump_flow real,
        calib_type real
    )
    """,
    'syserr':""" (dt timestamp PRIMARY KEY, 
        TimeStamp timestamp,
        Record bigint,
        err_message_str varchar(500)
    )
    """,
    'wug':""" (dt timestamp PRIMARY KEY, 
        temp real, 
        hum real, 
        vappres real,
        dewpt real,
        solrad real,
        netrad real,
        precip real,
        windres real,
        winddir real,
        windspd real,
        temp_pred real, 
        hum_pred real, 
        vappres_pred real,
        dewpt_pred real,
        precip_pred real,
        winddir_pred real,
        windspd_pred real,
        netrad_pred real
    ) 
    """  #netrad,netrad_pred = uv in WU, vappres_pred is mslp in WU, precip_pred is qpf in WU
}

class DBobj(object):
    '''A postgresql instance object
    Attributes:
        conn: A database connection
    '''

    #constructor of a DBobj object
    def __init__(self, dbname, pwd, host='localhost',user='postgres'):
        args = "dbname='{0}' user='{1}' host='{2}' password='{3}'".format(dbname,user,host,pwd)
        try:
            self.args = args
            self.conn = psycopg2.connect(args)
        except Exception as e:
            print(e)
            print('Problem connecting to DB')
            sys.exit(1)

    #reset the connection
    def reset(self):
        try:
            self.conn = psycopg2.connect(self.args)
        except Exception as e:
            print(e)
            print('Problem connecting to DB in reset')
            sys.exit(1)
    
    #return the cursor
    def get_cursor(self,svrcursor=None):
        if svrcursor:
            return self.conn.cursor(svrcursor)
        return self.conn.cursor()

    #commit the changes to the db
    def commit(self):
        if self.conn:
            self.conn.commit()

    #see if table exists, return True else False
    def table_exists(self,tablename): 
        curs = self.conn.cursor()
        curs.execute("select exists(select * from information_schema.tables where table_name=%s)", (tablename,))
        val = curs.fetchone()[0]
        return val

    #create a table
    def create_table(self,typename,tablename):
        curs = self.conn.cursor()
        typestring = TABLE_TYPE_MAP[typename]
        if typestring is None:
            print('Error: unable to create table {0}, no types in typemap: {1}'.format(tablename,TABLE_TYPE_MAP))
            return False
        try:
            curs.execute("DROP TABLE IF EXISTS {0}".format(tablename))
            curs.execute("CREATE TABLE {0} {1}".format(tablename,typestring))
        except Exception as e:
            print(e)
            print('Error: unable to create table {0}, in exceptional case. Type: \n{1}'.format(tablename,typestring))
            return False
        self.conn.commit()
        return True

    #create a TimeScaleDB table
    def create_tableTS(self,typename,tablename,colname): #colname must be type timestamp, date, or integer
        curs = self.conn.cursor()
        typestring = TABLE_TYPE_MAP[typename]
        if typestring is None:
            print('Error: unable to create table {0}, no types in typemap: {1}'.format(tablename,TABLE_TYPE_MAP))
            return False
        try:
            curs.execute("DROP TABLE IF EXISTS {0}".format(tablename))
            curs.execute("CREATE TABLE {0} {1}".format(tablename,typestring))
            curs.execute("SELECT create_hypertable({}, {})".format(tablename,colname))
        except Exception as e:
            print(e)
            print('Error: unable to create table (TSDB) {0}, in exceptional case. Type: \n{1}'.format(tablename,typestring))
            return False
        self.conn.commit()
        return True


    #delete a table
    def rm_table(self,tablename):
        curs = self.conn.cursor()
        try:
            curs.execute("DROP TABLE {0}".format(tablename))
        except:
            pass
        self.conn.commit()


    #invoke an SQL query on the db
    def execute_sql(self,sql):
        cur = self.conn.cursor()
        try:
            cur.execute(sql)
            self.conn.commit()
        except Exception as e:
            print(e)
            print('execute_sql: SQL problem:\n\t{0}'.format(sql))
            sys.exit(1)
        return cur

    #close the DB connection
    def closeConnection(self):
        if self.conn:
            self.conn.commit()
            self.conn.close()

def main():
    parser = argparse.ArgumentParser(description='Test a connection to a remote postgres DB')
    parser.add_argument('host',action='store',help='DB host IP')
    parser.add_argument('db',action='store',help='DB name')
    parser.add_argument('user',action='store',help='postgres username')
    parser.add_argument('pwd',action='store',help='postgres usernames password')
    parser.add_argument('--removetable',action='store_true',default=False,help='delete the table we create')
    args = parser.parse_args()
    
    #tests
    db = DBobj(args.db,args.pwd,args.host,args.user)
    sql = 'SELECT version()'
    cur = db.execute_sql(sql)
    ver = cur.fetchone()
    print(ver)

    tname = 'cimistest'
    print(db.table_exists(tname))
    retn = db.create_table('cimis',tname) #table type template is 'cimis' here, tname is table name; returns T/F
    cur = db.get_cursor()
    cur.execute("INSERT INTO {0} (dt,temp,hum,vappres,dewpt,solrad,netrad,eto,a_eto,a_etr,precip,windres,winddir,windspd,soil) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)".format(tname), 
        [datetime.now(),-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1])

    cur = db.get_cursor()
    cur.execute("SELECT * from {}".format(tname))
    rows = cur.fetchall()
    for row in rows:
        print(row)

    cur.close()
    db.commit()
    
    if args.removetable:
        db.rm_table(tname)
    db.closeConnection()

if __name__ == '__main__':
    main()
