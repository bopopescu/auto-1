#!/usr/bin/env ruby
def traverse_dir(file_path)  
  if File.directory? file_path  
    Dir.foreach(file_path) do |file|  
      if file!="." and file!=".."  
        traverse_dir(file_path+"/"+file){|x| yield x}  
      end  
    end  
  else  
    yield  file_path  
  end  
end  
  
s  = %q-.-  
old_path=''
traverse_dir(s){|f|  
 
# puts f  
 m=f.scan(/[^\/]*/)
 path=f.match(/.*(?=\/)/)
 #puts path
 if (path.to_s!=old_path.to_s)
   old_path=path
   tags=m[m.length-4]
  # puts tags
   content=m[m.length-2]
   # system "s=`cat \"#{f}\"`; echo $s; echo end"
#   system "~/@Work/Development/geeknote/gnsync.py --path \"#{path}\"  --notebook \"#{tags}\""
   print m
 end

} 
