from django.core.mail import EmailMessage


class Util:
  @staticmethod
  def send_email():
    email = EmailMessage(
      subject='hello',
      body='hii',
      from_email='ranjitshinde9404@gmail.com',
      to=['rohit.jadhav@weagile.net']
    )
    email.send()
    print('yess')

Util.send_email()