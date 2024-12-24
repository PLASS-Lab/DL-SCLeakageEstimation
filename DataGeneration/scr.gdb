target remote localhost:1234
set architecture arm
break main
continue
while 1
  stepi
  x/i $pc
end
