#!/bin/python
import smtplib,argparse

from passwords import PassPm # PassPm is a very simple class it and it consists this email = (email,password)

def Main ():
    parser = argparse.ArgumentParser(usage = './emailsend.py subject message --to email1 email2 emailN' )
    parser.add_argument('subject',  help='Give me a subject', type=str)
    parser.add_argument('message',  help='Give me a message', type=str)
    parser.add_argument('--to', nargs='+')
    args = parser.parse_args()
    sendEmail(args.subject,args.message,*args.to)

def sendEmail(subject, message,*toAddr):
    server = smtplib.SMTP('smtp.gmail.com', 587) 
    server.ehlo()
    server.starttls()
    temp = PassPm()
    print temp.email
    server.login(PassPm().email[0],PassPm().email[1])
    for addr in toAddr:
         
        msg ='To: %s\nSubject : %s\n%s' % (addr,subject,message)
        server.sendmail("efim@corporatecolo.com",addr, msg)
        print msg
    server.quit()


if __name__ == '__main__':
    Main()
