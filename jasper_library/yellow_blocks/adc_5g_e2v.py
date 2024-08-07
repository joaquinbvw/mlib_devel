from .yellow_block import YellowBlock
from verilog import VerilogModule
from constraints import PortConstraint, ClockConstraint, RawConstraint
from helpers import to_int_list
from .yellow_block_typecodes import *
import math

class adc_5g_e2v(YellowBlock):
    def initialize(self):
        self.provides = ['adc_clk','adc_clk90', 'adc_clk180', 'adc_clk270']
        if self.chips_num ==1:
            self.add_source('adc_5g_e2v/1chip/*.v')
            self.add_source('adc_5g_e2v/1chip/*.xci')
        else:
            self.add_source('adc_5g_e2v/2chips/*.v')
            self.add_source('adc_5g_e2v/2chips/*.xci')
        self.work_mode=1
        self.fmc_port=1
        if self.adc_mode=='1-Channel':
            self.work_mode=4
        elif self.adc_mode=='2-Channel':
            self.work_mode=2
        else:
            self.work_mode=1
        if self.adc_loc=="FMC1":
            self.fmc_port=1
        else:
            self.fmc_port=2

    def modify_top(self,top):
        module ='ad_top'
        inst = top.get_instance(entity=module, name=self.fullname, comment=self.fullname)
        if self.work_mode==1:
            inst.add_parameter('a_adcmode', "4'b0000   ")
        elif self.work_mode==2:
            inst.add_parameter('a_adcmode', "4'b0100   ")
        else:
            inst.add_parameter('a_adcmode', "4'b1000   ")

        if self.output_mode == 'test mode' :
            inst.add_parameter('a_outmode',  "1'b1   ")
        else:
            inst.add_parameter('a_outmode',  "1'b0   ")

        inst.add_parameter('a_offset_A', "16'h01FB   ")
        inst.add_parameter('a_offset_B', "16'h01CD   ")
        inst.add_parameter('a_offset_C', "16'h022C   ")
        inst.add_parameter('a_offset_D', "16'h0237   ")
        inst.add_parameter('a_gain_A',   "16'h0200   ")
        inst.add_parameter('a_gain_B',   "16'h021D   ")
        inst.add_parameter('a_gain_C',   "16'h023F   ")
        inst.add_parameter('a_gain_D',   "16'h0200   ")
        inst.add_parameter('a_phase_A',  "16'h0200   ")
        inst.add_parameter('a_phase_B',  "16'h0200   ")
        inst.add_parameter('a_phase_C',  "16'h0200   ")
        inst.add_parameter('a_phase_D',  "16'h0200   ")
        
        #top.add_signal('sys_rst_n')
        #top.assign_signal('sys_rst_n', '~sys_rst')
        
        inst.add_port('clk10m ', 'clk_10MHz'     )
        inst.add_port('clk10m_locked ', 'pll_lock'     )
        #inst.add_port('sys_rst_n   ', 'sys_rst_n'   )
        inst.add_port('sys_rst_n   ', 'ext_sys_rst_n', parent_port=True, dir='in')

        
        inst.add_port('ADR_P       ', 'adc_5g_chip1_adr_p'      , parent_port=True, dir='in')
        inst.add_port('ADR_N       ', 'adc_5g_chip1_adr_n'      , parent_port=True, dir='in')
        inst.add_port('AOR_P       ', 'adc_5g_chip1_aor_p'      , parent_port=True, dir='in')
        inst.add_port('AOR_N       ', 'adc_5g_chip1_aor_n'      , parent_port=True, dir='in')
        inst.add_port('BOR_P       ', 'adc_5g_chip1_bor_p'      , parent_port=True, dir='in')
        inst.add_port('BOR_N       ', 'adc_5g_chip1_bor_n'      , parent_port=True, dir='in')
        inst.add_port('COR_P       ', 'adc_5g_chip1_cor_p'      , parent_port=True, dir='in')
        inst.add_port('COR_N       ', 'adc_5g_chip1_cor_n'      , parent_port=True, dir='in')
        inst.add_port('DOR_P       ', 'adc_5g_chip1_dor_p'      , parent_port=True, dir='in')
        inst.add_port('DOR_N       ', 'adc_5g_chip1_dor_n'      , parent_port=True, dir='in')

        inst.add_port('A_P         ', 'adc_5g_chip1_a_p'        , parent_port=True, dir='in',width=10)
        inst.add_port('A_N         ', 'adc_5g_chip1_a_n'        , parent_port=True, dir='in',width=10)
        inst.add_port('B_P         ', 'adc_5g_chip1_b_p'        , parent_port=True, dir='in',width=10)
        inst.add_port('B_N         ', 'adc_5g_chip1_b_n'        , parent_port=True, dir='in',width=10)
        inst.add_port('C_P         ', 'adc_5g_chip1_c_p'        , parent_port=True, dir='in',width=10)
        inst.add_port('C_N         ', 'adc_5g_chip1_c_n'        , parent_port=True, dir='in',width=10)
        inst.add_port('D_P         ', 'adc_5g_chip1_d_p'        , parent_port=True, dir='in',width=10)
        inst.add_port('D_N         ', 'adc_5g_chip1_d_n'        , parent_port=True, dir='in',width=10)

        inst.add_port('adc_sclk    ', 'adc_5g_chip1_sclk'    ,  parent_port=True, dir='out')
        inst.add_port('adc_sen     ', 'adc_5g_chip1_sen'     ,  parent_port=True, dir='out')
        inst.add_port('adc_rst     ', 'adc_5g_chip1_rst'     ,  parent_port=True, dir='out')
        inst.add_port('adc_mosi    ', 'adc_5g_chip1_mosi'    ,  parent_port=True, dir='out')
        inst.add_port('adc_miso    ', 'adc_5g_chip1_miso'    ,  parent_port=True, dir='in' )
        inst.add_port('adc_sync    ', 'adc_5g_chip1_sync'    ,  parent_port=True, dir='out')
        inst.add_port('adc_sync_dir', 'adc_5g_chip1_sync_dir',  parent_port=True, dir='out')
            
        inst.add_port('a_dataA_0'         , self.fullname+'_ch0_data_a0', width=10)
        inst.add_port('a_dataA_1'         , self.fullname+'_ch0_data_a1', width=10)
        inst.add_port('a_dataA_2'         , self.fullname+'_ch0_data_a2', width=10)
        inst.add_port('a_dataA_3'         , self.fullname+'_ch0_data_a3', width=10)
        inst.add_port('a_dataB_0'         , self.fullname+'_ch0_data_b0', width=10)
        inst.add_port('a_dataB_1'         , self.fullname+'_ch0_data_b1', width=10)
        inst.add_port('a_dataB_2'         , self.fullname+'_ch0_data_b2', width=10)
        inst.add_port('a_dataB_3'         , self.fullname+'_ch0_data_b3', width=10)
        inst.add_port('a_dataC_0'         , self.fullname+'_ch0_data_c0', width=10)
        inst.add_port('a_dataC_1'         , self.fullname+'_ch0_data_c1', width=10)
        inst.add_port('a_dataC_2'         , self.fullname+'_ch0_data_c2', width=10)
        inst.add_port('a_dataC_3'         , self.fullname+'_ch0_data_c3', width=10)
        inst.add_port('a_dataD_0'         , self.fullname+'_ch0_data_d0', width=10)
        inst.add_port('a_dataD_1'         , self.fullname+'_ch0_data_d1', width=10)
        inst.add_port('a_dataD_2'         , self.fullname+'_ch0_data_d2', width=10)
        inst.add_port('a_dataD_3'         , self.fullname+'_ch0_data_d3', width=10)
        inst.add_port('data_valid'         , self.fullname+'_sync')
        inst.add_port('clk_data'         , 'adc_clk')
        inst.add_port('a_data_or'        ,'')

        top.add_signal('adc_clk270')
        top.assign_signal('adc_clk270', 'adc_clk') # just to match the requirement of toolflow
        top.add_signal('adc_clk90')
        top.assign_signal('adc_clk90', '~adc_clk270')
        top.add_signal('adc_clk180')
        top.assign_signal('adc_clk180', '~adc_clk')
  
        inst.add_port('flag_clk10m'         , 'flag_clk10m ')
        inst.add_port('flag_a_clk'          , 'flag_a_clk ')
        if self.chips_num ==2:
            inst.add_parameter('b_offset_A', "16'h0216   ")
            inst.add_parameter('b_offset_B', "16'h020F   ")
            inst.add_parameter('b_offset_C', "16'h01EA   ")
            inst.add_parameter('b_offset_D', "16'h026A   ")
            inst.add_parameter('b_gain_A',   "16'h0200   ")
            inst.add_parameter('b_gain_B',   "16'h01F5   ")
            inst.add_parameter('b_gain_C',   "16'h0226   ")
            inst.add_parameter('b_gain_D',   "16'h01FE   ")
            inst.add_parameter('b_phase_A',  "16'h0200   ")
            inst.add_parameter('b_phase_B',  "16'h0200   ")
            inst.add_parameter('b_phase_C',  "16'h0200   ")
            inst.add_parameter('b_phase_D',  "16'h0200   ")

            inst.add_port('ADR_P1       ', 'adc_5g_chip2_adr_p'      , parent_port=True, dir='in')
            inst.add_port('ADR_N1       ', 'adc_5g_chip2_adr_n'      , parent_port=True, dir='in')
            inst.add_port('AOR_P1       ', 'adc_5g_chip2_aor_p'      , parent_port=True, dir='in')
            inst.add_port('AOR_N1       ', 'adc_5g_chip2_aor_n'      , parent_port=True, dir='in')
            inst.add_port('BOR_P1       ', 'adc_5g_chip2_bor_p'      , parent_port=True, dir='in')
            inst.add_port('BOR_N1       ', 'adc_5g_chip2_bor_n'      , parent_port=True, dir='in')
            inst.add_port('COR_P1       ', 'adc_5g_chip2_cor_p'      , parent_port=True, dir='in')
            inst.add_port('COR_N1       ', 'adc_5g_chip2_cor_n'      , parent_port=True, dir='in')
            inst.add_port('DOR_P1       ', 'adc_5g_chip2_dor_p'      , parent_port=True, dir='in')
            inst.add_port('DOR_N1       ', 'adc_5g_chip2_dor_n'      , parent_port=True, dir='in')

            inst.add_port('A_P1         ', 'adc_5g_chip2_a_p'        , parent_port=True, dir='in',width=10)
            inst.add_port('A_N1         ', 'adc_5g_chip2_a_n'        , parent_port=True, dir='in',width=10)
            inst.add_port('B_P1         ', 'adc_5g_chip2_b_p'        , parent_port=True, dir='in',width=10)
            inst.add_port('B_N1         ', 'adc_5g_chip2_b_n'        , parent_port=True, dir='in',width=10)
            inst.add_port('C_P1         ', 'adc_5g_chip2_c_p'        , parent_port=True, dir='in',width=10)
            inst.add_port('C_N1         ', 'adc_5g_chip2_c_n'        , parent_port=True, dir='in',width=10)
            inst.add_port('D_P1         ', 'adc_5g_chip2_d_p'        , parent_port=True, dir='in',width=10)
            inst.add_port('D_N1         ', 'adc_5g_chip2_d_n'        , parent_port=True, dir='in',width=10)

            inst.add_port('adc_sclk1    ', 'adc_5g_chip2_sclk'    ,  parent_port=True, dir='out')
            inst.add_port('adc_sen1     ', 'adc_5g_chip2_sen'     ,  parent_port=True, dir='out')
            inst.add_port('adc_rst1     ', 'adc_5g_chip2_rst'     ,  parent_port=True, dir='out')
            inst.add_port('adc_mosi1    ', 'adc_5g_chip2_mosi'    ,  parent_port=True, dir='out')
            inst.add_port('adc_miso1    ', 'adc_5g_chip2_miso'    ,  parent_port=True, dir='in' )
            inst.add_port('adc_sync1    ', 'adc_5g_chip2_sync'    ,  parent_port=True, dir='out')
            inst.add_port('adc_sync_dir1', 'adc_5g_chip2_sync_dir',  parent_port=True, dir='out')
            
            inst.add_port('b_dataA_0'         , self.fullname+'_ch1_data_a0', width=10)
            inst.add_port('b_dataA_1'         , self.fullname+'_ch1_data_a1', width=10)
            inst.add_port('b_dataA_2'         , self.fullname+'_ch1_data_a2', width=10)
            inst.add_port('b_dataA_3'         , self.fullname+'_ch1_data_a3', width=10)
            inst.add_port('b_dataB_0'         , self.fullname+'_ch1_data_b0', width=10)
            inst.add_port('b_dataB_1'         , self.fullname+'_ch1_data_b1', width=10)
            inst.add_port('b_dataB_2'         , self.fullname+'_ch1_data_b2', width=10)
            inst.add_port('b_dataB_3'         , self.fullname+'_ch1_data_b3', width=10)
            inst.add_port('b_dataC_0'         , self.fullname+'_ch1_data_c0', width=10)
            inst.add_port('b_dataC_1'         , self.fullname+'_ch1_data_c1', width=10)
            inst.add_port('b_dataC_2'         , self.fullname+'_ch1_data_c2', width=10)
            inst.add_port('b_dataC_3'         , self.fullname+'_ch1_data_c3', width=10)
            inst.add_port('b_dataD_0'         , self.fullname+'_ch1_data_d0', width=10)
            inst.add_port('b_dataD_1'         , self.fullname+'_ch1_data_d1', width=10)
            inst.add_port('b_dataD_2'         , self.fullname+'_ch1_data_d2', width=10)
            inst.add_port('b_dataD_3'         , self.fullname+'_ch1_data_d3', width=10)
    
            inst.add_port('b_data_or'         , '')
            inst.add_port('trig_dir'          , self.fullname+'_trig_dir'    ,  parent_port=True, dir='out')
            inst.add_port('trig_ext'          , self.fullname+'_trig_ext'    ,  parent_port=True, dir='out')
            inst.add_port('flag_b_clk'          , 'flag_b_clk ')
            inst.add_port('flag_sync'          , 'flag_sync ')
    
    def gen_constraints(self):
        cons = [] 
        cons.append(PortConstraint('ext_sys_rst_n', 'ext_sys_rst_n'))
        cons.append(RawConstraint('set_property DIFF_TERM_ADV TERM_100 [get_ports {adc_5g_chip1_adr_p}]'))
        cons.append(RawConstraint('set_property DIFF_TERM_ADV TERM_100 [get_ports {adc_5g_chip1_aor_p}]'))
        cons.append(RawConstraint('set_property DIFF_TERM_ADV TERM_100 [get_ports {adc_5g_chip1_bor_p}]'))
        cons.append(RawConstraint('set_property DIFF_TERM_ADV TERM_100 [get_ports {adc_5g_chip1_cor_p}]'))
        cons.append(RawConstraint('set_property DIFF_TERM_ADV TERM_100 [get_ports {adc_5g_chip1_dor_p}]'))
        cons.append(RawConstraint('set_property DIFF_TERM_ADV TERM_100 [get_ports {adc_5g_chip1_a_p[0]}]'))
        cons.append(RawConstraint('set_property DIFF_TERM_ADV TERM_100 [get_ports {adc_5g_chip1_a_p[1]}]'))
        cons.append(RawConstraint('set_property DIFF_TERM_ADV TERM_100 [get_ports {adc_5g_chip1_a_p[2]}]'))
        cons.append(RawConstraint('set_property DIFF_TERM_ADV TERM_100 [get_ports {adc_5g_chip1_a_p[3]}]'))
        cons.append(RawConstraint('set_property DIFF_TERM_ADV TERM_100 [get_ports {adc_5g_chip1_a_p[4]}]'))
        cons.append(RawConstraint('set_property DIFF_TERM_ADV TERM_100 [get_ports {adc_5g_chip1_a_p[5]}]'))
        cons.append(RawConstraint('set_property DIFF_TERM_ADV TERM_100 [get_ports {adc_5g_chip1_a_p[6]}]'))
        cons.append(RawConstraint('set_property DIFF_TERM_ADV TERM_100 [get_ports {adc_5g_chip1_a_p[7]}]'))
        cons.append(RawConstraint('set_property DIFF_TERM_ADV TERM_100 [get_ports {adc_5g_chip1_a_p[8]}]'))
        cons.append(RawConstraint('set_property DIFF_TERM_ADV TERM_100 [get_ports {adc_5g_chip1_a_p[9]}]'))
        cons.append(RawConstraint('set_property DIFF_TERM_ADV TERM_100 [get_ports {adc_5g_chip1_b_p[0]}]'))
        cons.append(RawConstraint('set_property DIFF_TERM_ADV TERM_100 [get_ports {adc_5g_chip1_b_p[1]}]'))
        cons.append(RawConstraint('set_property DIFF_TERM_ADV TERM_100 [get_ports {adc_5g_chip1_b_p[2]}]'))
        cons.append(RawConstraint('set_property DIFF_TERM_ADV TERM_100 [get_ports {adc_5g_chip1_b_p[3]}]'))
        cons.append(RawConstraint('set_property DIFF_TERM_ADV TERM_100 [get_ports {adc_5g_chip1_b_p[4]}]'))
        cons.append(RawConstraint('set_property DIFF_TERM_ADV TERM_100 [get_ports {adc_5g_chip1_b_p[5]}]'))
        cons.append(RawConstraint('set_property DIFF_TERM_ADV TERM_100 [get_ports {adc_5g_chip1_b_p[6]}]'))
        cons.append(RawConstraint('set_property DIFF_TERM_ADV TERM_100 [get_ports {adc_5g_chip1_b_p[7]}]'))
        cons.append(RawConstraint('set_property DIFF_TERM_ADV TERM_100 [get_ports {adc_5g_chip1_b_p[8]}]'))
        cons.append(RawConstraint('set_property DIFF_TERM_ADV TERM_100 [get_ports {adc_5g_chip1_b_p[9]}]'))
        cons.append(RawConstraint('set_property DIFF_TERM_ADV TERM_100 [get_ports {adc_5g_chip1_c_p[0]}]'))
        cons.append(RawConstraint('set_property DIFF_TERM_ADV TERM_100 [get_ports {adc_5g_chip1_c_p[1]}]'))
        cons.append(RawConstraint('set_property DIFF_TERM_ADV TERM_100 [get_ports {adc_5g_chip1_c_p[2]}]'))
        cons.append(RawConstraint('set_property DIFF_TERM_ADV TERM_100 [get_ports {adc_5g_chip1_c_p[3]}]'))
        cons.append(RawConstraint('set_property DIFF_TERM_ADV TERM_100 [get_ports {adc_5g_chip1_c_p[4]}]'))
        cons.append(RawConstraint('set_property DIFF_TERM_ADV TERM_100 [get_ports {adc_5g_chip1_c_p[5]}]'))
        cons.append(RawConstraint('set_property DIFF_TERM_ADV TERM_100 [get_ports {adc_5g_chip1_c_p[6]}]'))
        cons.append(RawConstraint('set_property DIFF_TERM_ADV TERM_100 [get_ports {adc_5g_chip1_c_p[7]}]'))
        cons.append(RawConstraint('set_property DIFF_TERM_ADV TERM_100 [get_ports {adc_5g_chip1_c_p[8]}]'))
        cons.append(RawConstraint('set_property DIFF_TERM_ADV TERM_100 [get_ports {adc_5g_chip1_c_p[9]}]'))
        cons.append(RawConstraint('set_property DIFF_TERM_ADV TERM_100 [get_ports {adc_5g_chip1_d_p[0]}]'))
        cons.append(RawConstraint('set_property DIFF_TERM_ADV TERM_100 [get_ports {adc_5g_chip1_d_p[1]}]'))
        cons.append(RawConstraint('set_property DIFF_TERM_ADV TERM_100 [get_ports {adc_5g_chip1_d_p[2]}]'))
        cons.append(RawConstraint('set_property DIFF_TERM_ADV TERM_100 [get_ports {adc_5g_chip1_d_p[3]}]'))
        cons.append(RawConstraint('set_property DIFF_TERM_ADV TERM_100 [get_ports {adc_5g_chip1_d_p[4]}]'))
        cons.append(RawConstraint('set_property DIFF_TERM_ADV TERM_100 [get_ports {adc_5g_chip1_d_p[5]}]'))
        cons.append(RawConstraint('set_property DIFF_TERM_ADV TERM_100 [get_ports {adc_5g_chip1_d_p[6]}]'))
        cons.append(RawConstraint('set_property DIFF_TERM_ADV TERM_100 [get_ports {adc_5g_chip1_d_p[7]}]'))
        cons.append(RawConstraint('set_property DIFF_TERM_ADV TERM_100 [get_ports {adc_5g_chip1_d_p[8]}]'))
        cons.append(RawConstraint('set_property DIFF_TERM_ADV TERM_100 [get_ports {adc_5g_chip1_d_p[9]}]'))       

        clkconst = ClockConstraint('adc_5g_chip1_adr_p', 'adc_5g_chip1_adr_p', freq=self.f_sample/2/self.work_mode)
        cons.append(clkconst)

        if self.chips_num ==1:       
            cons.append(PortConstraint('adc_5g_chip1_adr_p', 'adc_5g_chip%d_adr_p'%self.fmc_port))
            cons.append(PortConstraint('adc_5g_chip1_aor_p', 'adc_5g_chip%d_aor_p'%self.fmc_port))
            cons.append(PortConstraint('adc_5g_chip1_bor_p', 'adc_5g_chip%d_bor_p'%self.fmc_port))
            cons.append(PortConstraint('adc_5g_chip1_cor_p', 'adc_5g_chip%d_cor_p'%self.fmc_port))
            cons.append(PortConstraint('adc_5g_chip1_dor_p', 'adc_5g_chip%d_dor_p'%self.fmc_port))
            cons.append(PortConstraint('adc_5g_chip1_a_p'  , 'adc_5g_chip%d_a_p'%self.fmc_port , port_index=list(range(10)), iogroup_index=list(range(10))))
            cons.append(PortConstraint('adc_5g_chip1_b_p'  , 'adc_5g_chip%d_b_p'%self.fmc_port , port_index=list(range(10)), iogroup_index=list(range(10))))
            cons.append(PortConstraint('adc_5g_chip1_c_p'  , 'adc_5g_chip%d_c_p'%self.fmc_port , port_index=list(range(10)), iogroup_index=list(range(10))))
            cons.append(PortConstraint('adc_5g_chip1_d_p'  , 'adc_5g_chip%d_d_p'%self.fmc_port , port_index=list(range(10)), iogroup_index=list(range(10))))

            cons.append(PortConstraint('adc_5g_chip1_sclk', 'adc_5g_chip%d_sclk'%self.fmc_port))
            cons.append(PortConstraint('adc_5g_chip1_sen' , 'adc_5g_chip%d_sen'%self.fmc_port))
            cons.append(PortConstraint('adc_5g_chip1_rst' , 'adc_5g_chip%d_rst'%self.fmc_port))
            cons.append(PortConstraint('adc_5g_chip1_mosi', 'adc_5g_chip%d_mosi'%self.fmc_port))
            cons.append(PortConstraint('adc_5g_chip1_miso', 'adc_5g_chip%d_miso'%self.fmc_port))
            cons.append(PortConstraint('adc_5g_chip1_sync', 'adc_5g_chip%d_sync'%self.fmc_port))
            cons.append(PortConstraint('adc_5g_chip1_sync_dir', 'adc_5g_chip%d_sync_dir'%self.fmc_port))
        else:#work in synchronization mode
            cons.append(PortConstraint('adc_5g_chip1_adr_p', 'adc_5g_chip1_adr_p'))
            cons.append(PortConstraint('adc_5g_chip1_aor_p', 'adc_5g_chip1_aor_p'))
            cons.append(PortConstraint('adc_5g_chip1_bor_p', 'adc_5g_chip1_bor_p'))
            cons.append(PortConstraint('adc_5g_chip1_cor_p', 'adc_5g_chip1_cor_p'))
            cons.append(PortConstraint('adc_5g_chip1_dor_p', 'adc_5g_chip1_dor_p'))
            cons.append(PortConstraint('adc_5g_chip1_a_p'  , 'adc_5g_chip1_a_p' , port_index=list(range(10)), iogroup_index=list(range(10))))
            cons.append(PortConstraint('adc_5g_chip1_b_p'  , 'adc_5g_chip1_b_p' , port_index=list(range(10)), iogroup_index=list(range(10))))
            cons.append(PortConstraint('adc_5g_chip1_c_p'  , 'adc_5g_chip1_c_p' , port_index=list(range(10)), iogroup_index=list(range(10))))
            cons.append(PortConstraint('adc_5g_chip1_d_p'  , 'adc_5g_chip1_d_p' , port_index=list(range(10)), iogroup_index=list(range(10))))

            cons.append(PortConstraint('adc_5g_chip1_sclk', 'adc_5g_chip1_sclk'))
            cons.append(PortConstraint('adc_5g_chip1_sen' , 'adc_5g_chip1_sen'))
            cons.append(PortConstraint('adc_5g_chip1_rst' , 'adc_5g_chip1_rst'))
            cons.append(PortConstraint('adc_5g_chip1_mosi', 'adc_5g_chip1_mosi'))
            cons.append(PortConstraint('adc_5g_chip1_miso', 'adc_5g_chip1_miso'))
            cons.append(PortConstraint('adc_5g_chip1_sync', 'adc_5g_chip1_sync'))
            cons.append(PortConstraint('adc_5g_chip1_sync_dir', 'adc_5g_chip1_sync_dir'))
            

            cons.append(PortConstraint('adc_5g_chip2_adr_p', 'adc_5g_chip2_adr_p'))
            cons.append(PortConstraint('adc_5g_chip2_aor_p', 'adc_5g_chip2_aor_p'))
            cons.append(PortConstraint('adc_5g_chip2_bor_p', 'adc_5g_chip2_bor_p'))
            cons.append(PortConstraint('adc_5g_chip2_cor_p', 'adc_5g_chip2_cor_p'))
            cons.append(PortConstraint('adc_5g_chip2_dor_p', 'adc_5g_chip2_dor_p'))
            cons.append(PortConstraint('adc_5g_chip2_a_p'  , 'adc_5g_chip2_a_p' , port_index=list(range(10)), iogroup_index=list(range(10))))
            cons.append(PortConstraint('adc_5g_chip2_b_p'  , 'adc_5g_chip2_b_p' , port_index=list(range(10)), iogroup_index=list(range(10))))
            cons.append(PortConstraint('adc_5g_chip2_c_p'  , 'adc_5g_chip2_c_p' , port_index=list(range(10)), iogroup_index=list(range(10))))
            cons.append(PortConstraint('adc_5g_chip2_d_p'  , 'adc_5g_chip2_d_p' , port_index=list(range(10)), iogroup_index=list(range(10))))

            cons.append(PortConstraint('adc_5g_chip2_sclk', 'adc_5g_chip2_sclk'))
            cons.append(PortConstraint('adc_5g_chip2_sen' , 'adc_5g_chip2_sen'))
            cons.append(PortConstraint('adc_5g_chip2_rst' , 'adc_5g_chip2_rst'))
            cons.append(PortConstraint('adc_5g_chip2_mosi', 'adc_5g_chip2_mosi'))
            cons.append(PortConstraint('adc_5g_chip2_miso', 'adc_5g_chip2_miso'))
            cons.append(PortConstraint('adc_5g_chip2_sync', 'adc_5g_chip2_sync'))
            cons.append(PortConstraint('adc_5g_chip2_sync_dir', 'adc_5g_chip2_sync_dir'))

            cons.append(PortConstraint(self.fullname+'_trig_dir', 'adc_5g_chip2_trig_dir'))
            cons.append(PortConstraint(self.fullname+'_trig_ext', 'adc_5g_chip2_trig_ext'))
            

            cons.append(RawConstraint('set_property DIFF_TERM_ADV TERM_100 [get_ports {adc_5g_chip2_adr_p}]'))
            cons.append(RawConstraint('set_property DIFF_TERM_ADV TERM_100 [get_ports {adc_5g_chip2_aor_p}]'))
            cons.append(RawConstraint('set_property DIFF_TERM_ADV TERM_100 [get_ports {adc_5g_chip2_bor_p}]'))
            cons.append(RawConstraint('set_property DIFF_TERM_ADV TERM_100 [get_ports {adc_5g_chip2_cor_p}]'))
            cons.append(RawConstraint('set_property DIFF_TERM_ADV TERM_100 [get_ports {adc_5g_chip2_dor_p}]'))
            cons.append(RawConstraint('set_property DIFF_TERM_ADV TERM_100 [get_ports {adc_5g_chip2_a_p[1]}]'))
            cons.append(RawConstraint('set_property DIFF_TERM_ADV TERM_100 [get_ports {adc_5g_chip2_a_p[2]}]'))
            cons.append(RawConstraint('set_property DIFF_TERM_ADV TERM_100 [get_ports {adc_5g_chip2_a_p[3]}]'))
            cons.append(RawConstraint('set_property DIFF_TERM_ADV TERM_100 [get_ports {adc_5g_chip2_a_p[4]}]'))
            cons.append(RawConstraint('set_property DIFF_TERM_ADV TERM_100 [get_ports {adc_5g_chip2_a_p[5]}]'))
            cons.append(RawConstraint('set_property DIFF_TERM_ADV TERM_100 [get_ports {adc_5g_chip2_a_p[6]}]'))
            cons.append(RawConstraint('set_property DIFF_TERM_ADV TERM_100 [get_ports {adc_5g_chip2_a_p[7]}]'))
            cons.append(RawConstraint('set_property DIFF_TERM_ADV TERM_100 [get_ports {adc_5g_chip2_a_p[8]}]'))
            cons.append(RawConstraint('set_property DIFF_TERM_ADV TERM_100 [get_ports {adc_5g_chip2_a_p[9]}]'))
            cons.append(RawConstraint('set_property DIFF_TERM_ADV TERM_100 [get_ports {adc_5g_chip2_b_p[0]}]'))
            cons.append(RawConstraint('set_property DIFF_TERM_ADV TERM_100 [get_ports {adc_5g_chip2_b_p[1]}]'))
            cons.append(RawConstraint('set_property DIFF_TERM_ADV TERM_100 [get_ports {adc_5g_chip2_b_p[2]}]'))
            cons.append(RawConstraint('set_property DIFF_TERM_ADV TERM_100 [get_ports {adc_5g_chip2_b_p[3]}]'))
            cons.append(RawConstraint('set_property DIFF_TERM_ADV TERM_100 [get_ports {adc_5g_chip2_b_p[4]}]'))
            cons.append(RawConstraint('set_property DIFF_TERM_ADV TERM_100 [get_ports {adc_5g_chip2_b_p[5]}]'))
            cons.append(RawConstraint('set_property DIFF_TERM_ADV TERM_100 [get_ports {adc_5g_chip2_b_p[6]}]'))
            cons.append(RawConstraint('set_property DIFF_TERM_ADV TERM_100 [get_ports {adc_5g_chip2_b_p[7]}]'))
            cons.append(RawConstraint('set_property DIFF_TERM_ADV TERM_100 [get_ports {adc_5g_chip2_b_p[8]}]'))
            cons.append(RawConstraint('set_property DIFF_TERM_ADV TERM_100 [get_ports {adc_5g_chip2_b_p[9]}]'))
            cons.append(RawConstraint('set_property DIFF_TERM_ADV TERM_100 [get_ports {adc_5g_chip2_c_p[0]}]'))
            cons.append(RawConstraint('set_property DIFF_TERM_ADV TERM_100 [get_ports {adc_5g_chip2_c_p[1]}]'))
            cons.append(RawConstraint('set_property DIFF_TERM_ADV TERM_100 [get_ports {adc_5g_chip2_c_p[2]}]'))
            cons.append(RawConstraint('set_property DIFF_TERM_ADV TERM_100 [get_ports {adc_5g_chip2_c_p[3]}]'))
            cons.append(RawConstraint('set_property DIFF_TERM_ADV TERM_100 [get_ports {adc_5g_chip2_c_p[4]}]'))
            cons.append(RawConstraint('set_property DIFF_TERM_ADV TERM_100 [get_ports {adc_5g_chip2_c_p[5]}]'))
            cons.append(RawConstraint('set_property DIFF_TERM_ADV TERM_100 [get_ports {adc_5g_chip2_c_p[6]}]'))
            cons.append(RawConstraint('set_property DIFF_TERM_ADV TERM_100 [get_ports {adc_5g_chip2_c_p[7]}]'))
            cons.append(RawConstraint('set_property DIFF_TERM_ADV TERM_100 [get_ports {adc_5g_chip2_c_p[8]}]'))
            cons.append(RawConstraint('set_property DIFF_TERM_ADV TERM_100 [get_ports {adc_5g_chip2_c_p[9]}]'))
            cons.append(RawConstraint('set_property DIFF_TERM_ADV TERM_100 [get_ports {adc_5g_chip2_d_p[0]}]'))
            cons.append(RawConstraint('set_property DIFF_TERM_ADV TERM_100 [get_ports {adc_5g_chip2_d_p[1]}]'))
            cons.append(RawConstraint('set_property DIFF_TERM_ADV TERM_100 [get_ports {adc_5g_chip2_d_p[2]}]'))
            cons.append(RawConstraint('set_property DIFF_TERM_ADV TERM_100 [get_ports {adc_5g_chip2_d_p[3]}]'))
            cons.append(RawConstraint('set_property DIFF_TERM_ADV TERM_100 [get_ports {adc_5g_chip2_d_p[4]}]'))
            cons.append(RawConstraint('set_property DIFF_TERM_ADV TERM_100 [get_ports {adc_5g_chip2_d_p[5]}]'))
            cons.append(RawConstraint('set_property DIFF_TERM_ADV TERM_100 [get_ports {adc_5g_chip2_d_p[6]}]'))
            cons.append(RawConstraint('set_property DIFF_TERM_ADV TERM_100 [get_ports {adc_5g_chip2_d_p[7]}]'))
            cons.append(RawConstraint('set_property DIFF_TERM_ADV TERM_100 [get_ports {adc_5g_chip2_d_p[8]}]'))
            cons.append(RawConstraint('set_property DIFF_TERM_ADV TERM_100 [get_ports {adc_5g_chip2_d_p[9]}]')) 
            clkconst = ClockConstraint('adc_5g_chip2_adr_p', 'adc_5g_chip2_adr_p', freq=self.f_sample/2/self.work_mode)
            cons.append(clkconst)

        return cons


 

        
