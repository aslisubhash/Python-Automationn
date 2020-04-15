from pages.accountDetails import AccountDetail
from pages.harbor import Harbor
from pages.opencccForm import OpencccForm
from pages.useful_functions import one_hack_banner, vpn_banner,get_email

'''
Hello


'''

one_hack_banner()
vpn_banner()

email = get_email()
print(email)
accountdetails = AccountDetail()
info = accountdetails.getInfo()
print(info)
print(email)
opencccForm = OpencccForm(info=info, email=email)
(username, password) = opencccForm.fill()

costa = Harbor(username, password, info)
costa.start_process()
