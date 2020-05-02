

import json
import csv
import os
import shutil
import re
from shutil import copyfile


#set directories   
# queue folder is the directory where the json should be exported from foundry
# latex_folder is where latex files should be written
# archive_folder is where jsons are placed once they have been transcribed to a latex

dir_path = os.path.dirname( os.path.realpath( __file__ ) )
queue_folder = dir_path + '\\jsonqueue\\'
latex_folder = dir_path + '\\Latex outputs\\'
archive_folder = dir_path +'\\jsonarchives\\'




# define function to chose an existing directory in the latex folder or create one if needed
def choose_latex_directory() :
    list_repertories_latex = []
    i = 0
    if int(batch_or_manual) == 0:
        list_repertories_latex.append('Where do you want to create this batch ? : \n[0} ADD NEW REPERT \n')
    else:
        list_repertories_latex.append( 'Where do you want to create file '+ filename + '? : \n[0} ADD NEW REPERT \n' )
    for repertory in os.listdir(latex_folder):
        i +=1
        repertory_choice = '['+str(i)+'] ' + repertory + '\n'
        list_repertories_latex.append(repertory_choice)
    while True :
        dir_latex = input(''.join(list_repertories_latex))
        try :
            int(dir_latex)
            if int(dir_latex) < 0 or int(dir_latex) > len(os.listdir(latex_folder)):
                raise ValueError ('Expected an integer between 0 and'+str(len(os.listdir(latex_folder)))+'please try again')
        except ValueError :
            print('Expected an integer between 0 and '+str(len(os.listdir(latex_folder)))+' please try again' )
        else :
            break

    if  int(dir_latex) == 0:
        new_dir = input('How do you want to name the new directory?')
        os.mkdir(latex_folder + new_dir)
        print('repertory '+ new_dir +' created')
        chosen_directory = new_dir+'\\'
        copyfile( dir_path +  '\\wfrp.sty', latex_folder + new_dir +  '\\wfrp.sty' )
        copyfile( dir_path + '\\' + 'wfrp-long.cls', latex_folder+new_dir + '\\' + 'wfrp-long.cls' )
        copyfile( dir_path + '\\' + 'NPCs.tex', latex_folder + new_dir + '\\' + 'NPCs.tex' )
        copyfile( dir_path + '\\' + 'main_document.tex', latex_folder + new_dir + '\\' + 'main_document.tex' )
    else :
        chosen_directory = os.listdir(latex_folder)[int(dir_latex)-1]+'\\'
    return (chosen_directory)

#count entities in the queue
count_queue = 0
for entity in os.listdir(queue_folder):
    if '.gitignore' in entity:
        print('gitignore was not counted')
    else:
        count_queue += 1

#Let user chose whether to:
# inport NPCs as a batch in one folder (batch_or_manual = 0)
# chose individually where to transcribe each file in the queue folder (batch_or_manual = 1)
batch_or_manual = 1
if count_queue > 1:
    while True :
        batch_or_manual = input( 'There are ' + str(count_queue ) + ' files in your queue folder, do you want to : \n[0] add them all to the same folder\n[1] add them individually to different folders' )
        try :
            batch_or_manual
            if int(batch_or_manual) != 0 and int(batch_or_manual) != 1 :
                raise ValueError('Expected 0 or 1, please try again')
        except ValueError:
            print('Expected 0 or 1, please try again')
        else :
            break

#chose directory to write in if batch import is enabled
if int(batch_or_manual)== 0:
   writing_destination = choose_latex_directory()


#define function to remove ligatures and html tags

def clean_text(x) :
    x = x.replace( 'ﬂ', 'fl' )
    x = x.replace( 'ﬀ', 'ff' )
    x = x.replace( 'ﬃ', 'ffi' )
    x= x.replace( 'ﬄ', 'ffl' )
    cleanr = re.compile('<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});')
    x = re.sub(cleanr,'',x)
    x.replace('\'','')
    return(x)


    return x


#looping over the files in the queue folder

for filename in os.listdir( queue_folder):
#ignore .gitignore
    if '.gitignore' in filename:
        print('.gitignored ignored')
    else:
    #define wrinting destination for the iterated file if batch writing is disabled
        if int(batch_or_manual) == 1:
            writing_destination = choose_latex_directory()
    #define a bunch of variables and lists that will be used inside of the loop for each actor
        name = filename
        skills = []
        score = []
        scoreinit = []
        scoreadv = []
        scoretot = []
        comp = []
        values = []
        listskills = []
        listtalents = []
        listspells = []
        listprayers = []
        listtrappings = []
        listtraits = []
        check = 0

    #open the actor json, utf8 encoding is resquired to read ligatures properly
        queued_item_path = queue_folder + filename
        with open( queued_item_path, 'r', encoding='utf-8' ) as json_file:
            pysheet = json.load( json_file )

    #find all data relative to the statblock of the NPC
        for key, value in pysheet['data']['characteristics'].items():
            scoreinit.append( value['initial'] )
            scoreadv.append( value['advances'] )
            scoretot.append( value['value'] )

        moveinit = pysheet['data']['details']['move']['value']
        movetot = pysheet['data']['details']['move']['value']
        woundstot = pysheet['data']['status']['wounds']['value']

        scoreinit.insert( 0, moveinit )
        scoretot.insert(0, movetot)
        scoretot.append( woundstot )

    #define function needed to remove ligature and unwanted html


    #loop over all item to stock the ones we need in corresponding lists
    #Talents and skills are added only if they have advances
    #traits takes in account the value  associated when there is one (i.e.Poison (5))


        for a in pysheet['items']:

            if a['type'] == 'skill' and a['data']['advances']['value'] > 0:
                tested = a['data']['characteristic']['value']
                test = pysheet['data']['characteristics'][str( tested )]['value'] + a['data']['advances']['value']
                skilltest = ' ' + a['name'] + '~' + str( test )
                listskills.append( skilltest )

            if a['type'] == 'talent' and a['data']['advances']['value'] > 0:
                tal = ' ' + a['name'] + '~' + str( a['data']['advances']['value'] )
                listtalents.append( tal )

            if a['type'] == 'trait':

                traitdesc = a['data']['description']['value']
                traitdesc = clean_text(traitdesc)


                if a['data']['specification']['value'] == '':
                    tr = a['name']
                    tr = clean_text( tr )
                    tr = '\\textbf{'+tr+'}~:~'+traitdesc+'\\\\'
                else:
                    tr = '\\textbf{'+a['name'] +' '+str( a['data']['specification']['value'] )+'}~:~'+traitdesc+'\\\\'
                    tr = clean_text( tr )



                listtraits.append( tr )

            if a['type'] == 'spell':
                spelldesc = a['data']['description']['value']
                spelldesc = spelldesc

                spel = '\\textbf{'+a['name']+'}' + ' (' + str( a['data']['range']['value'] ) + ',' + str(
                    a['data']['duration']['value'] ) + ',' + str( a['data']['target']['value'] ) + ')' + '~:~' + spelldesc+'\\\\'

                spel = clean_text(spel)
                listspells.append( spel )

                print(type(listspells))



            if a['type'] == 'prayer':
                prayerdesc = a['data']['description']['value']
                prayerdesc = prayerdesc
                pray = '\\textbf{'+a['name']+'}' + ' (' + str( a['data']['range']['value'] ) + ',' + str(
                    a['data']['duration']['value'] ) + ',' + str( a['data']['target']['value'] ) + ')' + '~:~' + prayerdesc+'\\\\'
                pray = clean_text(pray)
                listprayers.append( pray )


            if a['type'] == 'trapping' or a['type'] == 'weapon':
                trap = a['name']
                listtrappings.append( trap )

        print( listskills )
        print( listtalents )
        print( listtraits )
        print( scoretot)
        print( listspells )

    #write latex file

    #change name from extracted file to keep only the name chosen for the NPC
    #i.e; : fvtt-Actor-Karl_Franz.json --> karl_Franz

        cleanname = name.replace('fvtt-Actor-','')
        cleanname = cleanname.replace('.json','')
        cleanername = cleanname.replace('_',' ')

    #write on the latex
        with open( latex_folder + writing_destination +  cleanname + '.tex', 'w', newline='' ) as myfile:

            myfile.write('\statblock[h!]{' + cleanername + '}')
            myfile.write('\n' + '{')
            wr1 = csv.writer( myfile, quoting=csv.QUOTE_MINIMAL, delimiter='&' )
            wr1.writerow(scoretot)
            myfile.write( '}' )

            wr3 = csv.writer( myfile, quoting=csv.QUOTE_MINIMAL, delimiter='\n', quotechar= " ")
            wr2 = csv.writer( myfile, quoting=csv.QUOTE_MINIMAL )
            myfile.write( '\n' + '{' )
            wr3.writerow( listtraits )
            myfile.write( '}' )
            myfile.write( '\n' + '{' )
            wr2.writerow( listskills )
            myfile.write( '}' )
            myfile.write( '\n' + '{' )
            wr2.writerow( listtalents )
            myfile.write( '}' )
            myfile.write( '\n' + '{' )
            wr3.writerow( listspells )
            myfile.write( '}' )
            myfile.write( '\n' + '{' )
            wr3.writerow( listprayers )
            myfile.write( '}' )
            myfile.write( '\n' + '{' )
            wr2.writerow( listtrappings )
            myfile.write( '}' )

    #write name of tex file on the main NPC text file
        with open( latex_folder+writing_destination+'\\NPCs.tex', 'a', newline='' ) as myfile2:
         myfile2.write('\\input{'+cleanname+'}')

    #move the treated file from queue to archive
        archive_path = archive_folder + filename
        shutil.move(queued_item_path,archive_path)



