from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import subprocess
import codecs
import smtplib

# for p in psutil.process_iter():
#     print(p, p.name(), p.pid)

def enviar_mail(receiver_address:str, subject :str, mail_content:str,
                sender_address = 'smartpsystem@gmail.com', 
                ):   
    
    sender_pass = 'vtyrkfqciworubfg'

    try:
        #Setup the MIME
        message = MIMEMultipart()
        message['From'] = sender_address
        message['To'] = receiver_address
        message['Subject'] = subject  #The subject line
        #The body and the attachments for the mail
        message.attach(MIMEText(mail_content, 'html'))
        #Create SMTP session for sending the mail
        session = smtplib.SMTP('smtp.gmail.com', 587) #use gmail with port
        session.starttls() #enable security
        session.login(sender_address, sender_pass) #login with mail_id and password
        text = message.as_string()
        session.sendmail(sender_address, receiver_address, text)
        session.quit()
        print('Mail Sent')
    except Exception as excep:
        print('Exception: '+excep)
        print('Mail not sent!!. ')

def main():
    process_result = subprocess.check_output("ps -ef | grep Producer | awk '{print $2,$9,$11,$19}'", shell=True)
    process_result = codecs.decode(process_result)

    tres_cruces_devices = [
        '327671F2009776BE',
        'DD5F6C5BDA3D7A95',
        '4DE1C372D9293D6F',
        '9AA1AD57EC8B8856',
        '64ED8BB2354F293B',
        '51FE29B1E7DACCB6',
        '5AF3A94B18BC85EC',
        'CE6EFF5988ECBF74',
        'FCB85470B7C0E0CC'
    ]

    punta_carretas_devices = [
        '1450F8D346D80142',
        '6CD5B69AA55A998F',
        'F169C92836C6BD61',
        '8EC1B2C496D79789',
        '0587422811790E54',
        '3B6C05ACE681A093',
        '17665E7B44E5EFDC',
        '7E1C75F22B089FB9',
        '7A7C63A8F2813646'
    ]

    list_of_processes = process_result.split("\n")
    list_of_processes.pop()
    #print(list_of_processes)
    tres_cruces_activos = []
    punta_carretas_activos = []
    for p in list_of_processes:
        if 'Producer' in p and "TresCrucesShopping" in p:
            device = p.split(" ")[-1]
            tres_cruces_activos.append(device)
        elif 'Producer' in p and "PuntaCarretasShopping" in p:
            device = p.split(" ")[-1]
            punta_carretas_activos.append(device)

    if len(tres_cruces_activos) == len(tres_cruces_devices):
        print("todos los dispositivos de tres cruces se encuentran activos... !!")
    else:
        receiver = "pedrobonillo15@gmail.com; diazjose_80@hotmail.com; juandmattos@gmail.com"
        mail_content = f'''Estimado Soporte,<br><br>
        La generación de datos para el parking de <b>Tres Cruces Shopping</b> se encuentra <b>comprometida</b>!!!<br>
        De tal manera, se recomienda revisión manual dentro del sistema!!<br><br>
        Saludos Cordiales,<br>
        Smart Parking System<br><br>
        <i><b>NOTA:</b> este mensaje es generado de forma automática por la plataforma de monitoreo, no es necesaria la respuesta de este mail!!.<i>'''
        enviar_mail(subject="[ERROR] Generador de Datos SmartPSystem Alarmado!!", 
                    receiver_address=receiver, mail_content=mail_content)
    
    if len(punta_carretas_activos) == len(punta_carretas_devices):
        print("todos los dispositivos de punta carretas se encuentran activos... !!")
    else:
        receiver = "pedrobonillo15@gmail.com; diazjose_80@hotmail.com; juandmattos@gmail.com"
        mail_content = f'''Estimado Soporte,<br><br>
        La generación de datos para el parking de <b>Punta Carretas Shopping</b> se encuentra <b>comprometida</b>!!!<br>
        De tal manera, se recomienda revisión manual dentro del sistema!!<br><br>
        Saludos Cordiales,<br>
        Smart Parking System<br><br>
        <i><b>NOTA:</b> este mensaje es generado de forma automática por la plataforma de monitoreo, no es necesaria la respuesta de este mail!!.<i>'''
        enviar_mail(subject="[ERROR] Generador de Datos SmartPSystem Alarmado!!", 
                    receiver_address=receiver, mail_content=mail_content)


    

    

if __name__ == '__main__':
    main()