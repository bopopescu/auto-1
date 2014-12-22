#!/usr/bin/env Rscript
molecular=commandArgs(trailingOnly = TRUE)


energy_list_origin=read.csv(paste("energy_list_",molecular,".csv",sep=''))
loopnames=c('c98K','c198K','c298K')


for (loopname in loopnames){
  energy_list=energy_list_origin
  filename=paste(sep='',loopname,'_',molecular,'.csv')
  temp=read.csv(filename)
  
  
  energy_list=merge(energy_list,temp,by='Conformer')
  Gibbs=energy_list[,'Gibbs_cor']+energy_list[,'SP_Energy']
  energy_list=data.frame(energy_list,Gibbs)
  energy_list=with(energy_list,energy_list[order(Gibbs),])
  
  lowest_energy=as.numeric(energy_list[1,"Gibbs"])
  
  #  revelent_energy=sapply(energy_list$Gibbs,function(x){x-lowest_energy})
  Relative_Gibbs=(energy_list[,'Gibbs']-lowest_energy)*627.5095
 
  Relative_SP_Energy=(energy_list[,"SP_Energy"]-min(energy_list[,"SP_Energy"]))*627.5095
  weight=exp(-(Relative_Gibbs*4184)/(8.31451*98))
  Distribution=weight/sum(weight)
  Distribution=sprintf("%.1f%%",Distribution*100)
  Order=1:length(weight)
  energy_list=data.frame(energy_list,Relative_Gibbs,Distribution,Order,Relative_SP_Energy)
  
  output=energy_list[c('Order','Conformer','Relative_SP_Energy','Relative_Gibbs','Distribution')]
  filename=paste(sep='','Distribution',filename)
  write.csv(file=filename,output,row.names = FALSE)
}

