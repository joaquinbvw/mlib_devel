# 
# Synthesis run script generated by Vivado
# 

set_msg_config -id {HDL 9-1061} -limit 100000
set_msg_config -id {HDL 9-1654} -limit 100000
create_project -in_memory -part xc7z100ffg900-1

set_param project.singleFileAddWarning.threshold 0
set_param project.compositeFile.enableAutoGeneration 0
set_param synth.vivado.isSynthRun true
set_msg_config -source 4 -id {IP_Flow 19-2162} -severity warning -new_severity info
set_property webtalk.parent_dir C:/XilinxProjects/ip_repo/ADC08D1520_core/ADC08D1520_core.cache/wt [current_project]
set_property parent.project_path C:/XilinxProjects/ip_repo/ADC08D1520_core/ADC08D1520_core.xpr [current_project]
set_property XPM_LIBRARIES {XPM_CDC XPM_MEMORY} [current_project]
set_property default_lib xil_defaultlib [current_project]
set_property target_language Verilog [current_project]
set_property ip_repo_paths c:/XilinxProjects/ip_repo/ADC08D1520_core/ADC08D1520_core.srcs/sources_1 [current_project]
add_files c:/XilinxProjects/ip_repo/ADC08D1520_core/fake_data.coe
add_files -quiet c:/XilinxProjects/ip_repo/ADC08D1520_core/ADC08D1520_core.srcs/sources_1/ip/blk_mem_gen_0/blk_mem_gen_0.dcp
set_property used_in_implementation false [get_files c:/XilinxProjects/ip_repo/ADC08D1520_core/ADC08D1520_core.srcs/sources_1/ip/blk_mem_gen_0/blk_mem_gen_0.dcp]
read_ip -quiet C:/XilinxProjects/ip_repo/ADC08D1520_core/ADC08D1520_core.srcs/sources_1/ip/clk_wiz_0/clk_wiz_0.xci
set_property used_in_implementation false [get_files -all c:/XilinxProjects/ip_repo/ADC08D1520_core/ADC08D1520_core.srcs/sources_1/ip/clk_wiz_0/clk_wiz_0_board.xdc]
set_property used_in_implementation false [get_files -all c:/XilinxProjects/ip_repo/ADC08D1520_core/ADC08D1520_core.srcs/sources_1/ip/clk_wiz_0/clk_wiz_0.xdc]
set_property used_in_implementation false [get_files -all c:/XilinxProjects/ip_repo/ADC08D1520_core/ADC08D1520_core.srcs/sources_1/ip/clk_wiz_0/clk_wiz_0_ooc.xdc]
set_property is_locked true [get_files C:/XilinxProjects/ip_repo/ADC08D1520_core/ADC08D1520_core.srcs/sources_1/ip/clk_wiz_0/clk_wiz_0.xci]

read_ip -quiet C:/XilinxProjects/ip_repo/ADC08D1520_core/ADC08D1520_core.srcs/sources_1/ip/fifo_generator_0/fifo_generator_0.xci
set_property used_in_implementation false [get_files -all c:/XilinxProjects/ip_repo/ADC08D1520_core/ADC08D1520_core.srcs/sources_1/ip/fifo_generator_0/fifo_generator_0/fifo_generator_0_clocks.xdc]
set_property used_in_implementation false [get_files -all c:/XilinxProjects/ip_repo/ADC08D1520_core/ADC08D1520_core.srcs/sources_1/ip/fifo_generator_0/fifo_generator_0/fifo_generator_0.xdc]
set_property is_locked true [get_files C:/XilinxProjects/ip_repo/ADC08D1520_core/ADC08D1520_core.srcs/sources_1/ip/fifo_generator_0/fifo_generator_0.xci]

read_verilog -library xil_defaultlib {
  C:/XilinxProjects/ip_repo/ADC08D1520_core/ADC08D1520_core.srcs/sources_1/imports/src/async_input_sync.v
  C:/XilinxProjects/ip_repo/ADC08D1520_core/ADC08D1520_core.srcs/sources_1/imports/src/ADC_core_block.v
}
foreach dcp [get_files -quiet -all *.dcp] {
  set_property used_in_implementation false $dcp
}
read_xdc dont_touch.xdc
set_property used_in_implementation false [get_files dont_touch.xdc]

synth_design -top ADC_core_block -part xc7z100ffg900-1


write_checkpoint -force -noxdef ADC_core_block.dcp

catch { report_utilization -file ADC_core_block_utilization_synth.rpt -pb ADC_core_block_utilization_synth.pb }
