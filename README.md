# Foundry to WFRP_Tex
 A script that converts the json actors created on foundry-vtt to clean NPC sheets using WFRP_Tex (https://github.com/WFRPTeX/WFRPTeX)
 
1. Export your actor files from foundry vtt (right click on the actor and select export), choose the jsonqueue folder as destination. 
2. run the main script, if there is more than one json in your folder, you will be asked if you want to put them all in the same subdirectory in Latexoutput or if yoy want to give a destination manually to each file
3. You will have the option to create a new subdirectory if neeeded, the subdirectory will be created with all needed files to run the Latex properly
4. After the Latex are properly writen, the json file will be moved to the archive folder ;

If you create subdirectory manually,note that the Latex files need to be in the same subdirectory as wfrp.sty and wfrp-long.cls
The Latex structure consists in three nested latex: 
1: Each actor file contains the statblocr, it is named <youractor>.tex
2. The NPCs.tex file contains a list of the actor files with the input command (input{<youractor1>}, input{<youractor2},...)
3. The main_document file is a minimal WFRP_tex document that inputs NPCs in the chapter NPCs, if you compile it, you will get a pdf with all the statblocks of the actors that have been written in the fo      lder.                                                                                                                     
                                                                                                                           
                                                                                                                             
                                                                                                                             
