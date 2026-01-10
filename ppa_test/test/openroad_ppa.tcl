# OpenROAD script for PPA analysis with NanGate45 PDK

# Set paths to PDK files
set tech_lef "/root/autodl-tmp/OpenROAD-flow-scripts/flow/platforms/nangate45/lef/NangateOpenCellLibrary.tech.lef"
set std_cell_lef "/root/autodl-tmp/OpenROAD-flow-scripts/flow/platforms/nangate45/lef/NangateOpenCellLibrary.macro.lef"
set liberty_file "/root/autodl-tmp/OpenROAD-flow-scripts/flow/platforms/nangate45/lib/NangateOpenCellLibrary_typical.lib"

# Read technology and cell library
read_lef $tech_lef
read_lef $std_cell_lef
read_liberty $liberty_file

# Read the synthesized design
read_verilog design_nangate.v

# Link the design - making sure to use the specified top module
link_design comparator_3bit

# Try to detect if any clock port exists
set has_clock 0
set clock_period 10
set max_delay "N/A"
set found_clock_port ""

# Print all available ports for debugging
puts "Available ports in design:"
foreach port [get_ports *] {
    puts "  Port: $port"
}

# Look for common clock naming patterns
set clock_patterns {clk clock CLK CLOCK clk_i clock_i clk_in clock_in clock_net pclk aclk sys_clk}
foreach pattern $clock_patterns {
    set matching_ports [get_ports *$pattern*]
    if {[llength $matching_ports] > 0} {
        set found_clock_port [lindex $matching_ports 0]
        puts "Found clock port: $found_clock_port, creating clock with period $clock_period ns"
        create_clock -name clock -period $clock_period $found_clock_port
        set has_clock 1
        break
    }
}


# Generate reports
puts "Generating area report..."
report_design_area > area_report.txt

puts "Generating power report..."
if {$has_clock} {
    set_power_activity -global -activity 0.1
}
report_power > power_report.txt

# Run timing analysis
if {$has_clock} {
      report_checks -path_delay max -fields {net cap slew input_pins fanout} -format full_clock > timing_report.txt
      
      # Try to extract max path delay
      if {[file exists "timing_report.txt"]} {
          set timing_report [open "timing_report.txt" r]
          set report_content [read $timing_report]
          close $timing_report
          
          # Extract data arrival time from timing report
          if {[regexp {([0-9.]+)\s+data arrival time} $report_content match delay]} {
              set max_delay $delay
              puts "Extracted max path delay: $max_delay ns"
          } elseif {[regexp {slack\s+\([^)]+\)\s+([0-9.]+)} $report_content match slack]} {
              set max_delay [expr $clock_period - $slack]
              puts "Extracted max path delay from slack: $max_delay ns"
          } else {
              puts "Could not extract max path delay from timing report"
          }
      } else {
          puts "Warning: timing_report.txt file was not created!"
      }
} else {
    puts "No clock found, analyzing critical path for combinational circuit..."
    # Find critical path in combinational circuit
    report_checks -unconstrained -path_delay max -fields {net cap slew input_pins fanout} > timing_report.txt
    
    # Try to extract max path delay for combinational circuit
    if {[file exists "timing_report.txt"]} {
        set timing_report [open "timing_report.txt" r]
        set report_content [read $timing_report]
        close $timing_report
        
        # Extract delay information from unconstrained timing report
        if {[regexp {([0-9.]+)\s+data arrival time} $report_content match delay]} {
            set max_delay $delay
            puts "Extracted combinational critical path delay: $max_delay ns"
        } else {
            puts "Could not extract critical path delay from timing report"
        }
    } else {
        puts "Warning: timing_report.txt file was not created!"
    }
}

# Save timing information to a file
set timing_info [open "timing_metrics.txt" w]
puts $timing_info "MAX_DELAY=$max_delay"
puts $timing_info "HAS_CLOCK=$has_clock"
puts $timing_info "CLOCK_PERIOD=$clock_period"
if {$has_clock && [string length $found_clock_port] > 0} {
    puts $timing_info "CLOCK_PORT=$found_clock_port"
}
close $timing_info

puts "PPA Analysis completed."

# Exit OpenROAD
exit
