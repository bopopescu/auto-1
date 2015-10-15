#!/usr/bin/env ruby
$binpath=File.dirname(__FILE__).chomp
$etcpath=`cd #{$binpath}/../etc; pwd`.chomp
$st= "\033[31m"
$en= "\033[m"

def load_config(config_file_name,binpath=$binpath,etcpath=$etcpath)
 	config_file=nil  # real path and filename of config file, string, should use File#read()
	if File.exist?("#{config_file_name}")
		config_file="#{config_file_name}"
		puts "#{$st} use local #{config_file_name} #{$en}"
	elsif File.exist?("#{etcpath}/#{config_file_name}")
		config_file="#{etcpath}/#{config_file_name}"
		puts "#{$st} use #{etcpath}/#{config_file_name} #{$en}" 
	end
	return config_file
end
