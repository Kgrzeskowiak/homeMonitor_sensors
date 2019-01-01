from smsapi.client import SmsApiPlClient

client = SmsApiPlClient(access_token='Zxf0C6SLAIUtsH1t0h7xsDGudFIcoLXemNv6Xqsp')

r = client.sms.send(to='+48512087201', message='alarm')

print(r.id, r.points, r.status, r.error)