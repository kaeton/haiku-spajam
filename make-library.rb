#!/usr/bin/env ruby
# -*- coding: utf-8 -*-
# vim:set fileencoding=utf-8:

upperfile = "upper.csv"
middlefile = "middle.csv"
downfile = "down.csv"
writefile = ""

ARGF.each do |line|
    line.chomp!
    if line =~ /^upper/ then
        writefile = upperfile
    elsif line =~ /^middle/ then
        writefile = middlefile
    elsif line =~ /^down/ then
        writefile = downfile
    else 
        File.open(writefile, "a") { |f|
            f.puts(line)
        }
    
    end
end
